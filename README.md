ECDHE_RSA_AES_128_GCM_SHA256: Twisted vs HTTPServer
===================================================

Demonstrate that HTTPServer can successfully create connections with
`ECDHE_RSA_AES_128_GCM_SHA256`, while Twisted cannot.


Prepare
=======

You may need to install `twisted` and `curl`

     apt-get install -y python3-twisted curl

Prepare self-signed certificates in this folder

    ./bootstrap.sh


HTTPServer
==========

Run HTTPServer

    python3 https-server.py

Use `curl` to connect to that server. From a different window, from the same directory.

    curl -4 --ciphers ecdhe_rsa_aes_128_gcm_sha_256 --CAcert ca.crt --key dev.key  --cert dev.crt -v -v -v -v https://localhost:4443

Cipher is pinned to `ECDHE_RSA_AES_128_GCM_SHA256` both in `curl` and in `https-server.py`. Expected result is something like:

    * Rebuilt URL to: https://localhost:4443/
    *   Trying 127.0.0.1...
    * Connected to localhost (127.0.0.1) port 4443 (#0)
    * found 1 certificates in ca.crt
    * found 697 certificates in /etc/ssl/certs
    * ALPN, offering http/1.1
    * SSL connection using TLS1.2 / ECDHE_RSA_AES_128_GCM_SHA256
    * 	 server certificate verification OK
    * 	 server certificate status verification SKIPPED
    * 	 common name: localhost (matched)
    * 	 server certificate expiration date OK
    * 	 server certificate activation date OK
    * 	 certificate public key: RSA
    * 	 certificate version: #1
    * 	 subject: CN=localhost
    * 	 start date: Fri, 16 Sep 2016 18:16:58 GMT
    * 	 expire date: Fri, 30 Sep 2016 18:16:58 GMT
    *  	 issuer: CN=ca
    * 	 compression: NULL
    * ALPN, server did not agree to a protocol
    > GET / HTTP/1.1
    > Host: localhost:4443
    > User-Agent: curl/7.47.0
    > Accept: */*
    >
    * GnuTLS recv error (-110): The TLS connection was non-properly terminated.
    * Closing connection 0
    curl: (56) GnuTLS recv error (-110): The TLS connection was non-properly terminated.

The warning at the end is becaus the server does not set Content-Length.

It is quite clear which cipher is used:

    * SSL connection using TLS1.2 / ECDHE_RSA_AES_128_GCM_SHA256


Twisted
=======

With `twisted` the handshake is aborted:

    python3 twisted-server.py
    
The result is:

    * Rebuilt URL to: https://localhost:4443/
    *   Trying 127.0.0.1...
    * Connected to localhost (127.0.0.1) port 4443 (#0)
    * found 1 certificates in ca.crt
    * found 697 certificates in /etc/ssl/certs
    * ALPN, offering http/1.1
    * gnutls_handshake() failed: Handshake failed
    * Closing connection 0
    curl: (35) gnutls_handshake() failed: Handshake failed


Versions
========

Ubuntu 16.04 LTS
----------------

    Python 3.5.2 (default, Jul  5 2016, 12:43:10)
    [GCC 5.4.0 20160609] on linux
    
    Version('twisted', 16, 0, 0)
    
`http` from Python 3.5.2


OS X 10.11.6
------------

    Python 3.5.2 (default, Aug 16 2016, 05:35:40)
    [GCC 4.2.1 Compatible Apple LLVM 7.3.0 (clang-703.0.31)] on darwin

Debian Jessie
-------------

    Distributor ID:	Debian
    Description:	Debian GNU/Linux 8.5 (jessie)
    Release:	8.5
    Codename:	jessie
    
    Python 2.7.9 (default, Mar  1 2015, 12:57:24)
    [GCC 4.9.2] on linux2

    Version('twisted', 14, 0, 2)

    OpenSSL 1.0.1t  3 May 2016
