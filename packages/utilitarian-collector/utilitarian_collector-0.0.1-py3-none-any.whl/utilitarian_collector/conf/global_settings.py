import socketserver

"""
Global settings
"""

DEBUG = False

SERVER_CLASS = 'socketserver.UDPServer'
REQUEST_HANDLER = 'socketserver.BaseRequestHandler'

METER_MANAGERS = list()

PROTECTION_MANAGERS = list()

RESULT_MANAGERS = list()


# TODO: Handle settings of logging!
