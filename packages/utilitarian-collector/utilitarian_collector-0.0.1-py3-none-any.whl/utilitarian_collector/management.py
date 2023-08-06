import argparse
import socket

import os

import sys
import logging
import errno


from utilitarian_collector.servers import run


def execute_from_cli(argv=None):

    #TODO: handle args so it is easy to set up on different addres and port!

    parser = argparse.ArgumentParser(description='Supply Server Setting')
    parser.add_argument('--host', default='localhost',
                        help='Supply the address to bind the server to')
    parser.add_argument('--port', type=int, default=4059,
                        help='Supply the port to bind the server to')
    parser.add_argument('--async', action='store_true', default=False,
                        help='Say if the server is to be async')

    args = parser.parse_args(argv)

    try:
        run(args.host, args.port, threading=args.async)

    except socket.error as e:
        # Use helpful error messages instead of ugly tracebacks.
        ERRORS = {
            errno.EACCES: "You don't have permission to access that port.",
            errno.EADDRINUSE: "That port is already in use.",
            errno.EADDRNOTAVAIL: "That IP address can't be assigned to.",
        }
        try:
            error_text = ERRORS[e.errno]
        except KeyError:
            error_text = e

        print("Error: %s" % error_text)
        # Need to use an OS exit because sys.exit doesn't work in a thread
        os._exit(1)

    except KeyboardInterrupt:
        sys.exit(0)


