"""Create an HTTP server for providing the TPIR."""
import argparse
import logging
from logging.handlers import RotatingFileHandler

from aiohttp import web

from . import config
from .controller import Controller

logger = logging.getLogger('tpir')
fmt = '%(asctime)s\n%(levelname)s %(funcName)s:%(lineno)d\n%(message)s\n'
datefmt = '%I:%M:%S %p %Z, %d %b %Y'
logging.basicConfig(format=fmt, datefmt=datefmt, level=logging.WARNING)
logger.setLevel(logging.INFO)


async def root(request):
    """Serve index page."""
    return web.json_response(controller.get_state())


async def logs(request):
    """Serve logs page."""
    return web.Response(text=render_logs(config.log_path),
                        content_type='text/html')


def main():
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="A serial-to-ethernet server "
                                                 "for a ATMI TPIR sensor.")
    parser.add_argument('-p', '--port', type=int, default=80, help="The "
                        "port on which to serve the website. Defaults to "
                        "HTTP (80). Use external services like nginx to add "
                        "encryption and authentication.")
    choices = ['logging', 'all']
    parser.add_argument('-m', '--mock', nargs='*', choices=choices, default=[],
                        help="Runs the server with specified communication "
                             "interfaces mocked out. Use for local testing.")
    args = parser.parse_args()

    if 'all' in args.mock:
        args.mock = choices

    if not args.mock:
        h = RotatingFileHandler(config.log_path, maxBytes=2 ** 24, backupCount=5)
        h.setFormatter(logging.Formatter(fmt, datefmt))
        logger.addHandler(h)

    global controller
    controller = Controller(args.mock)

    app = web.Application()
    app.router.add_get('/', root)
    app.router.add_get('/log', logs)

    app.on_shutdown.append(controller.close)

    web.run_app(app, port=args.port)

def render_logs(path, controller_name, prettyprint=True):
    """Convert a log-formatted string into pretty-printed HTML.

    Edits include:
     * Most recent timestamp on top
     * Long error messages are truncated
    """
    with open(path) as in_file:
        logs = in_file.read()
    sorted_logs = logs.split('\n\n')[::-1]
    for i, log in enumerate(sorted_logs):
        if '\n' not in log:
            continue
        split = log.split('\n')
        if len(split) > 100:
            log = '\n'.join(split[:10] + ['[ ... ]'] + split[-10:])
        try:
            d = log.index('\n')
            sorted_logs[i] = f'<pre><b>{log[:d]}</b>{log[d:]}</pre>'
        except ValueError:
            pass
    return ''.join(sorted_logs)


if __name__ == '__main__':
    main()
