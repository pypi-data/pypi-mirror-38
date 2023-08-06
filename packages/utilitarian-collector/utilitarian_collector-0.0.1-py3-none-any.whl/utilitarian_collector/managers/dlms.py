

class DLMSProtectionManager:
    """
    Manager for different kinds of protection in DLMS. The manager will check
    the security context of the DLMS package and use the correct methods and
    parse the message to set the content.
    """

    supported_apdus = ['general-glo-cipher']

    def process_data(self, dlms_handler):
        handler = dlms_handler
        print('Running DLMSProtectionManager')

        if handler._apdu.name not in self.supported_apdus:
            raise NotImplemented('The APDU is not supported by this protection'
                                 ' manager')
        # TODO: need to check if encrypted and authenticated or just encrypted,
        # or just authenticated and if compressed. but should i be here or in

        if handler._encryption_key is None:
            raise ValueError('No encryption key accessible in the handler')
        if handler._authentication_key is None:
            raise ValueError('No authentication key accessible in the handler')

        content = handler._apdu.decrypt(handler._encryption_key,
                                        handler._authentication_key)

        handler._content = content








