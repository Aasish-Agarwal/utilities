#!/usr/bin/env python
import os
import time
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler


SERVERROOTDIR = '../src/test/robotframework/acceptance'
ROUTES = [
    ('/', SERVERROOTDIR)
]

class MyHandler(SimpleHTTPRequestHandler):

    def updateFile(self, data):
        #print ("\n\n***Inside updateFile***\n" + data)
        millis = int(round(time.time() * 1000))
        tempfile = "temp_" + `millis`
        f= open(tempfile ,"w+")
        f.write(data)
        f.close()
        firstfile = open("_firstpart","r")
        first = firstfile.read()
        lastfile = open("_lastpart","r")
        last = lastfile.read()
        data_to_store = first
        f = open(tempfile ,"r")
        f1 = f.readlines()
        f.close()
        os.remove(tempfile)
        count = 0
        value = ""
        docid = ""
        for x in f1:
            if count < 1:                
                docid = x
                docid = "" + docid
                docid = docid.rstrip()
                count = 1
            else:
                value = value + x
        data_to_store = data_to_store + '<div id=docid val="' + docid + '"></div>'
        data_to_store = data_to_store + '<div id="summernote">' + value + '</div>'
        data_to_store = data_to_store +  last
        print ("\n\n###" + docid + "###\n\n")
        filetoupdate = SERVERROOTDIR + '/' + docid
        f= open(filetoupdate , "w")
        f.write(data_to_store)
        f.close()

    def translate_path(self, path):
        # default root -> cwd        
        root = os.getcwd()
        
        # look up routes and get root directory
        for patt, rootDir in ROUTES:
            if path.startswith(patt):                
                path = path[len(patt):]
                root = rootDir
                break
        # new path
        return os.path.join(root, path)    

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        self.updateFile(body)
        #self.wfile.write(body)

if __name__ == '__main__':
    httpd = HTTPServer(('127.0.0.1', 8000), MyHandler)
    httpd.serve_forever()
