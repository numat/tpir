#!/usr/bin/env python
"""Interface between client calls and sensors/actuators. Stores state."""
import asyncio
import logging

from controllers.adapters.tpir import config
from controllers.adapters.tpir.interfaces import Tpir

logger = logging.getLogger('tpir')


class Controller:
    """A class for reading the TPIR."""

    def __init__(self, mock):
        """Initialize read task."""
        self.tpir = Tpir()
        self.task = asyncio.ensure_future(self._ir_loop())

    def get_state(self):
        """Return the current controller state, as a new object."""
        return self.state

    async def _ir_loop(self):
        """Read TPIR."""
        while True:
            await asyncio.sleep(config.read_delay)
            try:
                self.state = self.tpir.get()
            except Exception:
                self.state = [None] * 4
                logger.exception("Encountered error while reading.")

    async def close(self, *args):
        """Disconnect from devices and stops pending tasks."""
        self.task.cancel()
        try:
            await self.task
        except asyncio.CancelledError:
            pass
        self.tpir.close()
