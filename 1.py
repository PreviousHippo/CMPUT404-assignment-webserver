#  coding: utf-8
import SocketServer
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

    def checkHeader(self,request):
        MyRequest = self.data.split()
        method = MyRequest[0]
        root = MyRequest[1]
        protocol = MyRequest[2]

    def header_analysis(self, req):
        req_method, req_root, req_protocol = self.checkHeader(req)
        RootAbspath = os.path.abspath("www")

        #not access to the parent directory of root directory
        if root.startswith("/.."):
            self.ErrorMsg(protocol)

        #get the absolute path from the root
        else:
            if root[-1] == "/":
                abs_path = RootAbspath + root + "/index.html"
            else:
                abs_path = RootAbspath + root
            if method.upper() == "GET":
                self.Get(abs_path,protocol)






        """
        MyRequest = self.data.split()
        #print
        method = MyRequest[0]
        root = MyRequest[1]
        protocol = MyRequest[2]
        #print MyRequest
        #print root
        #get the absolute path from the root
        RootAbspath = os.path.abspath("www")

        #not access to the parent directory of root directory
        if root.startswith("/.."):
            self.ErrorMsg(protocol)

        #get the absolute path from the root
        else:
            if root[-1] == "/":
                abs_path = RootAbspath + root + "/index.html"
            else:
                abs_path = RootAbspath + root
            if method.upper() == "GET":
                self.Get(abs_path,protocol)
                """


    def ErrorMsg(self,protocol):
        Message = "HTTP/1.1 404 Not found\r\n\r\n"
        Message +="404 Not Found"
        self.request.sendall(Message)


    def Get(self,abs_path,protocol):
        try:
            FILE = open(abs_path, 'r')
            body = FILE.read()

            if abs_path.lower().endswith(".html"):
                mime = "text/html"

            elif abs_path.lower().endswith(".css"):
                mime = "text/css"

            Response = str(protocol)+" 200 OK\r\n"
            Response += "Content-Type: " + str(mime)+"\r\n"
            Response += "Content-Length: " + str(len(body)) +"\r\n"
            Response += "Connection: close" + "\r\n\r\n"
            Response += body + "\r\n"
            self.request.sendall(Response)
            FILE.close()

        # if the absolute path is not exist, throw the 404 error
        except:
            self.ErrorMsg(protocol)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
