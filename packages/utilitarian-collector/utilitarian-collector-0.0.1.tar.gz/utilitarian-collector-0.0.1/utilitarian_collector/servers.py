import logging
import socketserver

from utilitarian_collector.conf import settings
from utilitarian_collector.utils.module_loading import import_string

logger = logging.getLogger(__name__)


def run(address, port, threading=False):

    server_cls = import_string(settings.SERVER_CLASS)
    request_handler = import_string(settings.REQUEST_HANDLER)
    server_address = (address, port)

    if getattr(server_cls, 'use_asyncio'):
        # Starting asyncIO servers
        server = server_cls(server_address, request_handler)

    else:

        if threading:
            amr_server_cls = type('AMRServer', (socketserver.ThreadingMixIn, server_cls), {})
        else:
            amr_server_cls = server_cls

        server = amr_server_cls(server_address, request_handler)

        if threading:
            server.daemon_threads = True

    print(f'Running {server.__class__}  on {address}:{port}')
    server.serve_forever()

