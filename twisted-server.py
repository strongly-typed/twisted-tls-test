#!/usr/bin/env python3
from twisted.internet import ssl, reactor
from twisted.internet.protocol import Factory, Protocol

from OpenSSL.SSL import TLSv1_2_METHOD

class Echo(Protocol):
    def dataReceived(self, data):
        self.transport.write(data)

if __name__ == '__main__':

    myContextFactory = ssl.DefaultOpenSSLContextFactory(
        privateKeyFileName='srv.key',
        certificateFileName='srv.crt',
        sslmethod=TLSv1_2_METHOD
        )

    ctx = myContextFactory.getContext()

    ctx.set_cipher_list('ECDHE-RSA-AES128-GCM-SHA256')

    ctx.load_verify_locations("ca.crt")

    factory = Factory()
    factory.protocol = Echo

    reactor.listenSSL(4443, factory, myContextFactory)
    reactor.run()
