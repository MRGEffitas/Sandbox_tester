from distutils.core import setup
import py2exe, sys, os
import subprocess

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

data_files = [("",[mypath + "Microsoft.VC90.CRT.manifest", mypath + "msvcr90.dll"])]

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
command = '"C:\\Program Files\\WinRAR\\rar.exe" a -r -sfx -z"'+mypath+'sfx.cnf" sandbox_tester2.exe sandbox_tester.exe Microsoft.VC90.CRT.manifest msvcr90.dll w9xpopen.exe'
print(command)
print(run_command(command))