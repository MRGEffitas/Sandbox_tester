# Sandbox_tester


## Introduction
This package consists of a malware analysis sandbox tester tool, a DNS server and a HTTP server,
all written in Python. If the tool is executed on a sandbox, it will leak environment data to the 
configured servers. This information can be used to build better anti-sandbox solutions.

## Requirements
### Requirements on the HTTP/DNS server side
Python 2.7

### Requirements on the builder side
Python 2.7<br/>
py2exe, pywin32, PIL, requests<br/>
7Zip (7z binary added to PATH)

### Requirements in the malware execution environment
WinXP - Win10

## Quick setup guide
1. Change the global configuration variables in:<br/>
	global_config.ini<br/>

	target = `<YOUR_DOMAIN>`<br/>
	listen_ip = `<YOUR_IP>`

2. Setup DNS
	Let's say you own a domain called `<YOUR_DOMAIN`>, and you want to host your DNS and HTTP server on it,
	and you have the IP of `<YOUR_IP>`. The following config creates a new nameserver (ns.`<YOUR_DOMAIN>`) 
	which will resolve all subdomain requests to tt.`<YOUR_DOMAIN>`. This is needed to set up the DNS server.

	```
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
	```

3. Start the http_server.py and dns_server.py on your server.

4. Build a new executable with:
	python setup.py
	Locate your final executable in dist/sandbox_tester_sfx.exe

6. Upload sandbox_tester_sfx.exe to the sandbox, wait to finish analysis.

7. Check results in http.db, dns.db or in the report. If the result is in the report, 
use filename_decrypt_send.py on a txt file where the created filenames are listed. 

8. PROFIT!

##Help to decode the results:
  * aindesk: number of files in %USERPROFILE% 
  * bkmrk: non default bookmarks in IE
  * bm: WMI baseboard manufacturer, e.g. Hewlett-Packard
  * btt: WMI OS lastbootuptime (does not work on XP)
  * bv: WMI BIOS version, e.g. HPQOEM
  * cdr: WMI CDROM
  * cpc: WMI CPU core numbers
  * cpl: WMI CPU number of logical processors
  * cpn: WMI CPU name, e.g. Intel(R) Core(TM) i7-4702MQ CPU @ 2.40GHz
  * csm: WMI computersystem model, e.g. HP ProBook 450 G2
  * cst: WMI computersystem systemtype, e.g. x64-based PC
  * ddc: WMI diskdrive caption, e.g. TOSHIBA MQ01ABD075
  * ddm: WMI diskdrive model, e.g. TOSHIBA MQ01ABD075
  * ex: WMI process executablepath, e.g. C:\Windows\System32\cmd.exe
  * exec: current running process name
  * execp: current running process path
  * fsp: WMI logicaldisk freespace
  * fw1: Windows firewall state
  * fw2: Windows (XP) firewall state 
  * height: screen height
  * hookd: check whether windll.kernel32.DeleteFileW is hooked from user mode or not
  * hookr: check whether windll.advapi32.RegOpenKeyExA is hooked from user mode or not
  * id: WMI OS installation date
  * ldn: WMI logicaldisk name, e.g. C:, D:, E:
  * localport: check local port 445 is open or not
  * ls: WMI logicaldisk size
  * mac: network interface mace address
  * mon: WMI monitor name, e.g. Generic PnP Monitor
  * mouse1: mouse position
  * mouse2: mouse position some seconds later
  * oem: WMI computersystem OEMStringArray (this is rarely faked in VBOX/VMware)
  * ok: is the messagebox OK clicked? 
  * os: WMI OS caption, e.g. Microsoft Windows 8.1 Pro
  * pm: WMI computersystem totalphysicalmemory
  * pn: WMI product Name, installed products
  * pndrv: USB flash drives used in the sandbox
  * pr1: Windows proxy settings
  * pr2: Windows (XP) proxy settings
  * prn: WMI printer name, e.g. Canon MG7100 series Printer WS
  * pvn: WMI logicaldisk providername
  * rinappd: number of recently modified files (last 7 days) in %APPDATA%
  * rindesk: number of recently modified files (last 7 days) in Desktop
  * rindoc: number of recently modified files (last 7 days) in Documents
  * rinlocappd: number of recently modified files (last 7 days) in %LOCALAPPDATA%
  * rintemp: number of recently modified files (last 7 days) in %TEMP%
  * rrg: number of recently modified files based on the registry
  * sleepworks: check whether sleep is emulated or not
  * sn: WMI OS serialnumber
  * snd: WMI sound device, e.g. IDT High Definition Audio CODEC
  * sye: WMI systemenclosure manufacturer, e.g. Hewlett-Packard
  * time: current time on the sandbox
  * user: curren username
  * userdom: current user domain or hostname
  * vbio: VIDEOBIOSVERSION from registry (this is rarely faked in VBOX/VMware)
  * width: screen width
  * wint: applications with GUI Windows
  