import glob
import subprocess
#...
#Build StdLib.DLL
ipath = r'c:\Bin\IronPython2.7'
ipyc = ipath + r'\ipyc.exe'
# any library files you need
gb = []
gb += glob.glob( ipath + r".\Lib\*.py")
gb += glob.glob( ipath + r".\Lib\encodings\*.py")
# ...
gb = [ipyc,"/main:StdLib.py","/embed","/platform:x86","/target:dll"] + gb
subprocess.call(gb)
print (gb)
print ("Made StdLib")