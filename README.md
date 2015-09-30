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
  * AINDESK: number of files in %USERPROFILE% 
  * BKMRK: non default bookmarks in IE
  * BM: WMI baseboard manufacturer, e.g. Hewlett-Packard
  * BTT: WMI OS lastbootuptime (does not work on XP)
  * BV: WMI BIOS version, e.g. HPQOEM
  * CDR: WMI CDROM
  * CPC: WMI CPU core numbers
  * CPL: WMI CPU number of logical processors
  * CPN: WMI CPU name, e.g. Intel(R) Core(TM) i7-4702MQ CPU @ 2.40GHz
  * CSM: WMI computersystem model, e.g. HP ProBook 450 G2
  * CST: WMI computersystem systemtype, e.g. x64-based PC
  * DDC: WMI diskdrive caption, e.g. TOSHIBA MQ01ABD075
  * DDM: WMI diskdrive model, e.g. TOSHIBA MQ01ABD075
  * EX: WMI process executablepath, e.g. C:\Windows\System32\cmd.exe
  * EXEC: current running process name
  * EXECP: current running process path
  * FSP: WMI logicaldisk freespace
  * FW1: Windows firewall state
  * FW2: Windows (XP) firewall state 
  * HEIGHT: screen height
  * HOOKD: check whether windll.kernel32.DeleteFileW is hooked from user mode or not
  * HOOKR: check whether windll.advapi32.RegOpenKeyExA is hooked from user mode or not
  * ID: WMI OS installation date
  * LDN: WMI logicaldisk name, e.g. C:, D:, E:
  * LOCALPORT: check local port 445 is open or not
  * LS: WMI logicaldisk size
  * MAC: network interface mace address
  * MON: WMI monitor name, e.g. Generic PnP Monitor
  * MOUSE1: mouse position
  * MOUSE2: mouse position some seconds later
  * OEM: WMI computersystem OEMStringArray (this is rarely faked in VBOX/VMware)
  * OK: is the messagebox OK clicked? 
  * OS: WMI OS caption, e.g. Microsoft Windows 8.1 Pro
  * PM: WMI computersystem totalphysicalmemory
  * PN: WMI product Name, installed products
  * PNDRV: USB flash drives used in the sandbox
  * PR1: Windows proxy settings
  * PR2: Windows (XP) proxy settings
  * PRN: WMI printer name, e.g. Canon MG7100 series Printer WS
  * PVN: WMI logicaldisk providername
  * RINAPPD: number of recently modified files (last 7 days) in %APPDATA%
  * RINDESK: number of recently modified files (last 7 days) in Desktop
  * RINDOC: number of recently modified files (last 7 days) in Documents
  * RINLOCAPPD: number of recently modified files (last 7 days) in %LOCALAPPDATA%
  * RINTEMP: number of recently modified files (last 7 days) in %TEMP%
  * RRG: number of recently modified files based on the registry
  * SLEEPWORKS: check whether sleep is emulated or not
  * SN: WMI OS serialnumber
  * SND: WMI sound device, e.g. IDT High Definition Audio CODEC
  * SYE: WMI systemenclosure manufacturer, e.g. Hewlett-Packard
  * TIME: current time on the sandbox
  * USER: curren username
  * USERDOM: current user domain or hostname
  * VBIO: VIDEOBIOSVERSION from registry
  * WIDTH: screen width
  * WINT: applications with GUI Windows
  

## Known issues
  * Some commands are buggy on XP - but it is safe to assume that if it is XP it is a sandbox ;) 
  * Some results are not forwarded on non-english systems, like russian or chinese
