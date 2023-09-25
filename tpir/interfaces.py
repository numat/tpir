"""Read the ATMI TPIR."""
from threading import Event, Thread

import serial


class Tpir:
    """Python driver for ATMI TPIR gas sensor.

    This communicates with the device over a USB-interfaced RS-232/RS-485
    connection using pyserial.
    """

    def __init__(self, port='/dev/ttyUSB0'):
        """Connect this driver with the appropriate USB / serial port.

        Args:
            port: The serial port. Default '/dev/ttyUSB0'.

        """
        self.connection = serial.Serial(port, 4800, timeout=1.0)
        self.buffer = ''
        self.state = None
        self.thread_event = Event()
        self.thread = Thread(target=self._read)
        self.thread.daemon = True
        self.thread.start()

    def get(self):
        """Get the current state of the sensor.

        This sensor is set up as a pub-sub interface. This dictates the
        cadence of reading, which doesn't play well with scheduling reads from
        other RS-232 devices. To get around, this class constantly reads the
        stream in a background thread. Calling `get` simply returns the most
        recently stored values.

        For now, I'm throwing out all the data outside of the four channels.
        There are 18 columns that are logged, but no documentation suggesting
        what they correspond to.

        Returns:
            The raw intensity values of the four sensors, as a list of ints.

        """
        return self.state

    def _read(self):
        """Handle sensor data publication in background."""
        while not self.thread_event.is_set():
            size = self.connection.inWaiting()
            if size > 0:
                self.buffer += self.connection.read(size).decode('utf-8')
            if '\r' in self.buffer:
                line, self.buffer = self.buffer.split('\r', 1)
                self.state = [int(x) if x else 0
                              for x in line.split(',')[6:10]]
            self.thread_event.wait(0.1)

    def close(self):
        """Close the serial port. Call this on program termination."""
        self.thread_event.set()
        self.connection.flush()
        self.connection.close()
