#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl, socket

bindsocket = socket.socket()
bindsocket.bind(('', 4443))
bindsocket.listen(5)

ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
ssl_context.options = ssl.PROTOCOL_TLSv1_2
# ssl_context.set_alpn_protocols(['http/1.1'])
# ssl_context.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384')
# ssl_context.set_ciphers('ECDHE-ECDSA-AES128-GCM-SHA256')
ssl_context.set_ciphers('ECDHE-RSA-AES128-GCM-SHA256')

# Use this private key to authenticate the server against the client
ssl_context.load_cert_chain(certfile='srv.crt', keyfile='srv.key')

# Expect that the client has the private key corresponding to that certificate
# ssl_context.load_verify_locations(cafile='ca.crt')
# ssl_context.load_verify_locations(cafile='dev.crt')
# ssl_context.verify_mode = ssl.CERT_REQUIRED
# ssl_context.verify_flags = ssl.VERIFY_X509_STRICT | ssl.VERIFY_CRL_CHECK_CHAIN

def do_something(connstream, data):
	print('Do Something:', data)
	return False

def deal_with_client(connstream):
	data = connstream.read()
	while data:
		if not do_something(connstream, data):
			break
		data = connstream.read()

while True:
	newsock, fromaddr = bindsocket.accept()
	ssl_socket = ssl_context.wrap_socket(newsock, server_side=True)

	try:
		deal_with_client(ssl_socket)
	finally:
		ssl_socket.shutdown(socket.SHUT_RDWR)
		ssl_socket.close()

