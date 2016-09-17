#!/usr/bin/env python3
import sys

from twisted.internet import ssl, protocol, task, defer, reactor
from twisted.internet.endpoints import SSL4ServerEndpoint

from OpenSSL import SSL, crypto

from twisted.python import log


class Echo(protocol.Protocol):
    def dataReceived(self, data):
        self.transport.write(data)

def main(reactor):
    log.startLogging(sys.stdout)

    with open('srv.crt') as certFile:
        # serverCert = ssl.Certificate.loadPEM(certFile.read())
        serverCert = crypto.load_certificate(type=crypto.FILETYPE_PEM, buffer=certFile.read())

    with open('srv.key') as keyFile:
        with open('srv.crt') as certFile:
            # serverKey = ssl.PrivateCertificate.loadPEM(keyFile.read() + certFile.read())
            serverKey = crypto.load_privatekey(type=crypto.FILETYPE_PEM, buffer=keyFile.read())

    with open('ca.crt') as certFile:
        caCert = ssl.Certificate.loadPEM(certFile.read())

    cipherListString = 'ECDHE-RSA-AES128-GCM-SHA256'
    acceptableCiphers = ssl.AcceptableCiphers.fromOpenSSLCipherString(cipherListString)

    trustRoot = ssl.trustRootFromCertificates([caCert])
    
    options = ssl.CertificateOptions(
        certificate=serverCert,
        privateKey=serverKey,
        trustRoot=trustRoot,
        acceptableCiphers=acceptableCiphers,
        method=SSL.TLSv1_2_METHOD
        )

    factory = protocol.Factory.forProtocol(Echo)

    endpoint = SSL4ServerEndpoint(reactor, 4443, options)
    endpoint.listen(factory)

    reactor.run()
    return defer.Deferred()

if __name__ == '__main__':
    task.react(main)
