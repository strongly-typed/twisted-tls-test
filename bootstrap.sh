#!/usr/bin/env bash

openssl genrsa -out ca.key 2048
openssl req -x509 -new -nodes -key ca.key -sha256 -days 14 -out ca.crt -batch -subj "/CN=ca"

openssl genrsa -out dev.key 2048
openssl req -new -key dev.key -out dev.csr -batch -subj "/CN=localhost"
openssl x509 -req -in dev.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out dev.crt -days 14

openssl genrsa -out srv.key 2048
openssl req -new -key srv.key -out srv.csr -batch -subj "/CN=localhost"
openssl x509 -req -in srv.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out srv.crt -days 14
