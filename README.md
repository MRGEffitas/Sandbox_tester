# Sandbox_tester


## Introduction:
This package consists of a malware analysis sandbox tester tool, a DNS server and a HTTP server,
all written in Python. If the tool is executed on a sandbox, it will leak environment data to the 
configured servers. This information can be used to build better anti-sandbox solutions.

## Requirements
### Requirements on the HTTP/DNS server side:
Python 2.7

### Requirements on the builder side:
Python 2.7
py2exe, pywin32, PIL, requests
7Zip (7z binary added to PATH)

### Requirements in the malware execution environment:
WinXP - Win10

##Quick setup guide:
1. Change the global (and optionally local) configuration variables in:
	http_server.py
	dns_server.py
	sandbox_tester.py

target = <YOUR_DOMAIN>
listen_ip = <YOUR_IP>

2. Setup DNS:
Let's say you own a domain called <YOUR_DOMAIN>, and you want to host your DNS and HTTP server on it,
and you have the IP of <YOUR_IP>. The following config creates a new nameserver (ns.<YOUR_DOMAIN>) 
which will resolve all subdomain requests to tt.<YOUR_DOMAIN>. This is needed to set up the 

A (Host):
	host: @
	points to: <YOUR_IP>

	host: tt
	points to: <YOUR_IP>

Cname(Alias):
	host: ns
	Points to: @

NS record:
	host: tt
	points to: ns.<YOUR_DOMAIN>


3. Start the http_server.py and dns_server.py on your server.

4. Build a new executable with:
	python setup.py
Locate your final executable in dist/sandbox_tester_sfx.exe

6. Upload sandbox_tester_sfx.exe to the sandbox, wait to finish analysis.

7. Check results in http.db, dns.db or in the report. 

8. PROFIT!