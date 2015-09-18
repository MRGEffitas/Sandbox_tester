from distutils.core import setup
import py2exe, sys, os
import subprocess
from sys import platform as _platform

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

sys.argv.append('py2exe')

mypath = 'C:\\devel\\eclipse_workspace_2\\python_scripts\\sandbox_mapping\\'

data_files = [("",[mypath + "Microsoft.VC90.CRT.manifest", mypath + "msvcr90.dll"
                   , mypath + "7zS.sfx", mypath + "config.txt", mypath + "global_config.ini"])]

setup(
    data_files=data_files,
    options = {'py2exe': {'bundle_files': 1,'compressed': True, #'ascii':True,
                           'excludes':[
     'pyreadline', 'difflib', 'doctest',  
     'optparse', 'pickle']}},
    windows = [{'script': "sandbox_tester.py"}],
    zipfile = None,

)

os.chdir(mypath + '/dist')
if _platform == "linux" or _platform == "linux2":
    # create .7z file
    command = '7z a sandbox_tester.7z sandbox_tester.exe Microsoft.VC90.CRT.manifest msvcr90.dll global_config.ini'
    print(command)
    print(run_command(command))
    # concat sfx + config + 7z
    command = "cat 7zS.sfx config.txt sandbox_tester.7z > sandbox_tester_sfx.exe"
    print(command)
    print(run_command(command))
    
else:
    #command = '"C:\\Program Files\\WinRAR\\rar.exe" a -r -sfx -z"'+mypath+'sfx.cnf" sandbox_tester_sfx.exe sandbox_tester.exe Microsoft.VC90.CRT.manifest msvcr90.dll w9xpopen.exe'
        # create .7z file
    command = 'C:\\Program Files (x86)\\7-Zip\\7z.exe a sandbox_tester.7z sandbox_tester.exe Microsoft.VC90.CRT.manifest msvcr90.dll global_config.ini'
    print(command)
    print(run_command(command))
    # concat sfx + config + 7z
    command = 'cmd /c "copy /B 7zS.sfx + config.txt + sandbox_tester.7z sandbox_tester_sfx.exe"'
    print(command)
    print(run_command(command))
    