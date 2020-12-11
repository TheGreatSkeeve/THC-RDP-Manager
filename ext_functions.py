import glob
import ntpath
import subprocess
import winreg
from pathlib import Path

import PySimpleGUI as sg
import wincertstore

connectionDirectory = "./connections/"
Path(connectionDirectory).mkdir(parents=True, exist_ok=True)

exe = "mstsc.exe"
userentry = "username:s:"
passentry = "password 51:b:"
hostentry = "full address:s:"
multientry = "use multimon:i:"

newCert = "New-SelfSignedCertificate -subject \"CN=Steve's RDP Manager\" -CertStoreLocation Cert:\CurrentUser\My -FriendlyName \"Steve's RDP Manager\" -NotAfter (Get-Date).AddYears(10)"

getThumb = '''
$x = Get-ChildItem  -Path Cert:\CurrentUser\My | Where-Object {$_.Subject -Match \"Steve's\"} | Select-Object Thumbprint
$x = $x.thumbprint
$x
'''

def set_reg(name, value):
    REG_PATH = r"SOFTWARE\Microsoft\Terminal Server Client\PublisherBypassList"
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                       winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_DWORD, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False

# Get a list of the RDP Files in the Connections folder
def getFiles():
    filelist = glob.glob("connections/" + '*.rdp')
    namesonly = []
    for file in filelist:
        name = (ntpath.basename(file)).split(".", 1)
        namesonly.append(name[0])
    return namesonly

currentlist = getFiles()

# Manually connect to a server via IP and port
def connectRDP_Manual(IP, port):
    connection = exe + " /v:" + str(IP) + ":" + str(port)
    powershellRun(connection)


# Run a Powershell command / open a file with Powershell
def powershellRun(filename):
    process = subprocess.Popen('powershell.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(filename.encode('utf-8'))
    return out

# Write an RDP file
def createRDP(filename, contents,sign):
    try:
        with open(filename, "w") as f:
            f.write(contents)
            f.close()
    except Exception as e:
        print(e)
    if sign=="sign":
        thumb = certCheck()
        command = "rdpsign /sha256 "+thumb+" "+filename
        powershellRun(command)



# Creates a new cert
# Called if certCheck cannot find the cert in the personal store
# Returns thumbprint of cert
def certSetup():
    try:
        powershellRun(newCert)
        out = powershellRun(getThumb)
        out = [x.decode("utf8") for x in out.split(b"$x\n") if len(x) > 35]
        last = out[1].split("\r", 1)
        thumbprint = last[0]
    except:
        print("Something went wrong with generating the cert")
    try:
        set_reg(thumbprint+"00", 0x0000004c)
    except:
        print("Something went wrong trusting the cert")
    return thumbprint

#Find if the "Steve's RDP Manager" cert is in the provided store
def certCount(storename):
    store = wincertstore.CertSystemStore(storename)
    count = 0
    for cert in store.itercerts():
        if "Steve's RDP Manager" in cert.get_name():
            count += 1
    return count


# Returns personal cert thumbprint, generates cert if necessery
def certCheck():
    count = certCount("MY")
    if count >0:
        out = powershellRun(getThumb)
        out = [x.decode("utf8") for x in out.split(b"$x\n") if len(x) > 35]
        last = out[1].split("\r", 1)
        thumbprint = last[0]
    if count == 0:
        thumbprint = certSetup()
    root_add()
    return thumbprint

def root_add():
    count = certCount("ROOT")
    if count == 0:
        window2 = sg.Window("Alert",[
            [sg.Text("We're going to install the application's cert in your Trusted Root Certificate Authorities, please approve the next prompt.")],
            [sg.OK()]
        ])
        window2.read()
        window2.close()
        powershellRun("./addroot.ps1")

# Encrypt a password provided by the user
# This is only decryptable by the Windows user who created it, on the computer they created it on
def encryptPassword(password):
    command = '''
    $x = (convertto-securestring -string "%s" -asplaintext -force | convertfrom-securestring)
    write-host $x
    '''
    command = command % password
    out = powershellRun(command)
    output = [x.decode("utf8") for x in out.split(b"\n") if len(x) > 200]
    secureString = output[0]
    return secureString


def parseRDP(rdpfile):
    returned = [None] * 5
    if "connections" in rdpfile:
        filename = rdpfile + ".rdp"
    else:
        filename = "connections/" + rdpfile + ".rdp"
    openme = open(filename, "r")
    for i in range(0, 5):
        line = openme.readline()
        if "full address" in line:
            line = line.split(":")
            x = line[2].split("\n")
            returned[0] = (x[0])
        if "username" in line:
            line = line.split(":")
            x = line[2].split("\n")
            returned[1] = (x[0])
        if "password" in line:
            line = line.split(":")
            x = line[2].split("\n")
            returned[2] = (x[0])
    return returned
