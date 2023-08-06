import socketserver
import threading

from dlms_cosem.wrappers import UDPWrapper

from utilitarian_collector.handlers import BaseDLMSHandler


class UDPRequestHandler(socketserver.BaseRequestHandler):

    _amr_handler_cls = BaseDLMSHandler

    def handle(self):
        data = self.request[0]
        cur_thread = threading.current_thread()
        print(
            "Received Datagram in in thread {} from {}:{} :".format(
                cur_thread.name,
                self.client_address[0],
                self.client_address[1],
            )
        )
        udp_wrapper = UDPWrapper.from_bytes(data)
        handler = self._amr_handler_cls(udp_wrapper.dlms_data)
        handler.add_source_info(self.client_address[0], self.client_address[1])
        handler.process_data()