import sys
import os.path
import uuid
from glob import glob, escape
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote
import re


class HttpServer:
    def __init__(self):
        self.sessions = {}
        self.types = {}
        self.types['.pdf'] = 'application/pdf'
        self.types['.jpg'] = 'image/jpeg'
        self.types['.txt'] = 'text/plain'
        self.types['.html'] = 'text/html'

    def response(self, kode=404, message='Not Found', messagebody=bytes(), headers={}):
        tanggal = datetime.now().strftime('%c')
        resp = []
        resp.append("HTTP/1.0 {} {}\r\n".format(kode, message))
        resp.append("Date: {}\r\n".format(tanggal))
        resp.append("Connection: close\r\n")
        resp.append("Server: myserver/1.0\r\n")
        resp.append("Content-Length: {}\r\n".format(len(messagebody)))
        for kk in headers:
            resp.append("{}:{}\r\n".format(kk, headers[kk]))
        resp.append("\r\n")

        response_headers = ''
        for i in resp:
            response_headers = "{}{}".format(response_headers, i)
        # menggabungkan resp menjadi satu string dan menggabungkan dengan messagebody yang berupa bytes
        # response harus berupa bytes
        # message body harus diubah dulu menjadi bytes
        if (type(messagebody) is not bytes):
            messagebody = messagebody.encode()

        response = response_headers.encode() + messagebody
        # response adalah bytes
        return response

    def proses(self, data):

        requests = data.split("\r\n")
        # print(requests)

        baris = requests[0]
        # print(baris)

        all_headers = [n for n in requests[1:] if n != '']

        j = baris.split(" ")
        try:
            method = j[0].upper().strip()
            if (method == 'GET'):
                object_address = j[1].strip()
                return self.http_get(object_address, all_headers)
            if (method == 'POST'):
                object_address = j[1].strip()
                return self.http_post(object_address, all_headers)
            else:
                return self.response(400, 'Bad Request', '', {})
        except IndexError:
            return self.response(400, 'Bad Request', '', {})

    def http_get(self, object_address, headers):
        object_address = unquote(object_address)

        if (object_address == '/'):
            return self.response(200, 'OK', 'Ini Adalah Web Server Percobaan', dict())

        print(f"ADDRESS : {object_address}")
        files = glob('./**/*')
        for i in files:
            print(i)
        filename = '.' + object_address.replace("/", "\\")

        if filename not in files:
            return self.response(404, 'Not Found', '', {})

        fp = open(filename, 'rb')
        isi = fp.read()

        fext = os.path.splitext(filename)[1]
        content_type = self.types[fext]
        headers = {}
        headers['Content-type'] = content_type

        return self.response(200, 'OK', isi, headers)

    def http_post(self, object_address, headers):
        headers = {}
        isi = "kosong"
        return self.response(200, 'OK', isi, headers)

if __name__ == "__main__":
    httpserver = HttpServer()
    # d = httpserver.proses('GET / HTTP/1.0')
    # print(d)
    d = httpserver.proses('GET /images/pokijan.jpg HTTP/1.0')
    print(d)
