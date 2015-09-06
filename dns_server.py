#!/usr/bin/env python
import socket
import sqlite3
import sys
import traceback
import datetime
import atexit
import traceback
from sys import platform as _platform

#Global config
key = 'ANOTHERONEGOTCAUGHTTODAYITSALLOVERTHEPAPERSTEENAGERARRESTEDINCOMPUTERCRIMESCANDALHACKERARRESTEDAFTERBANKTAMPERINGDAMNKIDSTHEYREALLALIKEBUTDIDYOUINYOURTHREEPIECEPSYCHOLOGYANDSTECHNOBRAINEVERTAKEALOOKBEHINDTHEEYESOFTHEHACKERDIDYOUEVERWONDERWHATMADEHIMTICKWHATFORCESSHAPEDHIMWHATMAYHAVEMOLDEDHIMIAMAHACKERENTERMYWORLDMINEISAWORLDTHATBEGINSWITHSCHOOLIMSMARTERTHANMOSTOFTHEOTHERKIDSTHISCRAPTHEYTEACHUSBORESMEDAMNUNDERACHIEVERTHEYREALLALIKEIMINJUNIORHIGHORHIGHSCHOOLIVELISTENEDTOTEACHERSEXPLAINFORTHEFIFTEENTHTIMEHOWTOREDUCEAFRACTIONIUNDERSTANDITNOMSSMITHIDIDNTSHOWMYWORKIDIDITINMYHEADDAMNKIDPROBABLYCOPIEDITTHEYREALLALIKEIMADEADISCOVERYTODAYIFOUNDACOMPUTERWAITASECONDTHISISCOOLITDOESWHATIWANTITTOIFITMAKESAMISTAKEITSBECAUSEISCREWEDITUPNOTBECAUSEITDOESNTLIKEMEORFEELSTHREATENEDBYMEORTHINKSIMASMARTASSORDOESNTLIKETEACHINGANDSHOULDNTBEHEREDAMNKIDALLHEDOESISPLAYGAMESTHEYREALLALIKEANDTHENITHAPPENEDADOOROPENEDTOAWORLDRUSHINGTHROUGHTHEPHONELINELIKEHEROINTHROUGHANADDICTSVEINSANELECTRONICPULSEISSENTOUTAREFUGEFROMTHEDAYTODAYINCOMPETENCIESISSOUGHTABOARDISFOUNDTHISISITTHISISWHEREIBELONGIKNOWEVERYONEHEREEVENIFIVENEVERMETTHEMNEVERTALKEDTOTHEMMAYNEVERHEARFROMTHEMAGAINIKNOWYOUALLDAMNKIDTYINGUPTHEPHONELINEAGAINTHEYREALLALIKEYOUBETYOURASSWEREALLALIKEWEVEBEENSPOONFEDBABYFOODATSCHOOLWHENWEHUNGEREDFORSTEAKTHEBITSOFMEATTHATYOUDIDLETSLIPTHROUGHWEREPRECHEWEDANDTASTELESSWEVEBEENDOMINATEDBYSADISTSORIGNOREDBYTHEAPATHETICTHEFEWTHATHADSOMETHINGTOTEACHFOUNDUSWILLINGPUPILSBUTTHOSEFEWARELIKEDROPSOFWATERINTHEDESERTTHISISOURWORLDNOWTHEWORLDOFTHEELECTRONANDTHESWITCHTHEBEAUTYOFTHEBAUDWEMAKEUSEOFASERVICEALREADYEXISTINGWITHOUTPAYINGFORWHATCOULDBEDIRTCHEAPIFITWASNTRUNBYPROFITEERINGGLUTTONSANDYOUCALLUSCRIMINALSWEEXPLOREANDYOUCALLUSCRIMINALSWESEEKAFTERKNOWLEDGEANDYOUCALLUSCRIMINALSWEEXISTWITHOUTSKINCOLORWITHOUTNATIONALITYWITHOUTRELIGIOUSBIASANDYOUCALLUSCRIMINALSYOUBUILDATOMICBOMBSYOUWAGEWARSYOUMURDERCHEATANDLIETOUSANDTRYTOMAKEUSBELIEVEITSFOROUROWNGOODYETWERETHECRIMINALSYESIAMACRIMINALMYCRIMEISTHATOFCURIOSITYMYCRIMEISTHATOFJUDGINGPEOPLEBYWHATTHEYSAYANDTHINKNOTWHATTHEYLOOKLIKEMYCRIMEISTHATOFOUTSMARTINGYOUSOMETHINGTHATYOUWILLNEVERFORGIVEMEFORIAMAHACKERANDTHISISMYMANIFESTOYOUMAYSTOPTHISINDIVIDUALBUTYOUCANTSTOPUSALLAFTERALLWEREALLALIKE'
target = 'sndbxtst.info'  #target domain for leak <YOUR_DOMAIN>
url_end = '/sndbxtst/index.php'
url_screenshot_end = "/sndbxtst/scrn.php"
subdomain = '.tt.'

#Local config
listen_ip = '0.0.0.0'       #listen on all interfaces <YOUR_IP>
logfile = 'dns.txt'         #debug log
config_dbfile = 'dns.db'    #path to sqlite
ip='127.0.0.1'              #return this IP as response to lookup 

def exit_handler():
    print("Exiting")
    udps.close()
    if con:
        con.close()

atexit.register(exit_handler)

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

class DNSQuery:
  def __init__(self, data):
    self.data=data
    self.domain=''

    tipo = (ord(data[2]) >> 3) & 15   # Opcode bits
    if tipo == 0:                     # Standard query
      ini=12
      lon=ord(data[ini])
      while lon != 0:
        self.domain+=data[ini+1:ini+lon+1]+'.'
        ini+=lon+1
        lon=ord(data[ini])

  def response(self, ip):
    packet=''
    if self.domain:
      packet+=self.data[:2] + "\x81\x80"
      packet+=self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'   # Questions and Answers Counts
      packet+=self.data[12:]                                         # Original Domain Name Question
      packet+='\xc0\x0c'                                             # Pointer to domain name
      packet+='\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'             # Response type, ttl and resource data length -> 4 bytes
      packet+=str.join('',map(lambda x: chr(int(x)), ip.split('.'))) # 4bytes of IP
    return packet

if __name__ == '__main__':

    print 'dom.query. 60 IN A %s' % ip    
    #if _platform == "linux" or _platform == "linux2":
    dbfile = config_dbfile
    #else:
    #    dbfile = 'dns.db'
    
    con = sqlite3.connect(dbfile)
    
    cur = con.cursor()   
    try:  
        cur.execute("SELECT * FROM data")
        rows = cur.fetchall()
        for row in rows:
            print "old " + ','.join(str(i) for i in row)
            pass
        
        #cur.execute("DROP TABLE if exists data ")  
    except:
        print ('sqlite table did not exist')
    try:
        cur.execute("CREATE TABLE data(sessionid varchar, type varchar, value varchar, requestdate date, ip varchar)")
        cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS MyUniqueIndex ON data (sessionid,type,value)")
    except:
        traceback.print_exc()
        print ('sqlite create error')
    try:    
        if con:
            con.close()
    except:
        pass                
    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #if _platform == "linux" or _platform == "linux2":
    udps.bind((listen_ip,53))     
    #else:
    #    udps.bind(('',53))
    while 1:
        try:
             
           data, addr = udps.recvfrom(1024)
           p=DNSQuery(data)

           if p.domain.find(target) > -1 :
                 udps.sendto(p.response(ip), addr)
                 print 'Response: %s -> %s' % (p.domain, ip)                 
                 fullinfo, domain = p.domain.split(target)
                 print (fullinfo)
                 fullinfo = fullinfo.replace("'","")
                 info, session,temp, temp2 = fullinfo.split('.')            
                 decrypted = translateMessage(info,key,'decrypt')
                 type, value = decrypted.split('-',1)
                 print (type,value)
                 type = type.upper()
                 con = sqlite3.connect(dbfile)
                 cur = con.cursor()  
                 try:               
                     cur.execute("INSERT INTO data (sessionid, type, value, requestdate, ip) VALUES(?,?,?,?,?)", 
                         (session,type.upper(),value,str(datetime.datetime.utcnow()), str(addr[0])))
                     con.commit()
                 except sqlite3.IntegrityError:
                     print("Ierr")
                     if con:
                         try:
                             con.close()
                         except:
                             pass
                     continue
                 try:
                     if con:
                         con.close()
                 except:
                     pass
        except:
            with open(logfile, "a") as myfile: 
                traceback.print_exc(file=myfile)
            traceback.print_exc()