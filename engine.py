import glob
import ntpath
import subprocess
from pathlib import Path

import PySimpleGUI as sg

connectionDirectory = "./connections/"
Path(connectionDirectory).mkdir(parents=True, exist_ok=True)
exe = "mstsc.exe"
userentry = "username:s:"
passentry = "password 51:b:"
hostentry = "full address:s:"
multientry = "use multimon:i:"


# Get a list of the RDP Files in the Connections folder
def getFiles():
    filelist = glob.glob("connections/" + '*.rdp')
    namesonly = []
    for file in filelist:
        name = (ntpath.basename(file)).split(".", 1)
        namesonly.append(name[0])
    return namesonly


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
def createRDP(filename, contents):
    with open(filename, "w") as f:
        f.write(contents)
        f.close()


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


##############################
# GUI Stuff
##############################
Button_Open = sg.Button("Connect", key='-Button_Open-', bind_return_key=True)
Button_Quit = sg.Button("Quit", key='-Button_Quit-', bind_return_key=True)

sg.theme('SystemDefault')

# Add RDP Connection Section
newRDP_Text = sg.Text("Create a new RDP Connection")
newRDP_Name = sg.Text("Choose a name")
newRDP_NameInput = sg.InputText(key='-newRDP_NameInput-')
newRDP_IP = sg.Text("Enter IP Address:port")
newRDP_IPInput = sg.InputText(key='-newRDP_IPInput-')
newRDP_User = sg.Text("Enter username")
newRDP_UserInput = sg.InputText(key='-newRDP_UserInput-')
newRDP_Pass = sg.Text("Enter password")
newRDP_PassInput = sg.InputText(key='-newRDP_PassInput-')
newRDP_Button_Save = sg.Button("Save as new connection", key="-newRDP_Button_Save-", bind_return_key=True)
newSettings_fullscreen = sg.Text("Fullscreen?")
newSettings_fullscreenInput = sg.CBox('', size=(10, 15), key="-newSettings_fullscreenInput-")

# Create and populate current RDP connection listbox
x = getFiles()
listbox_browse = sg.Listbox(values=x, size=(30, 15), select_mode=sg.SELECT_MODE_EXTENDED, key='demolist')
listbox_text = sg.Text("Saved Connections:", font='Helvetica 13', )

column_connections = sg.Col([[listbox_text], [listbox_browse], [Button_Open]])

column_new = sg.Col([
    [newRDP_Text], [newRDP_Name, newRDP_NameInput], [newRDP_IP, newRDP_IPInput], [newRDP_User, newRDP_UserInput],
    [newRDP_Pass, newRDP_PassInput], [newSettings_fullscreen, newSettings_fullscreenInput], [newRDP_Button_Save]])

devOutput = sg.Output(size=(125, 15), font='Helvetica 10', key='_output_', visible=True)
devOuputText = sg.Text("Console Output / Errors:")
column_dev = sg.Col([[devOuputText], [devOutput]])

##############################
# Define the GUI
##############################
layout = [
    [column_connections, column_new],
    [column_dev]
]

window = sg.Window(
    'RDP Console', layout,
    default_element_size=(30, 2), resizable=True,
    font=('Helvetica', ' 13'),
    default_button_element_size=(4, 1),
    return_keyboard_events=True
)


def main():
    while True:
        event, value = window.read()
        if event in (sg.WIN_CLOSED, 'EXIT'):
            window.close()
            break

        elif event == '-Button_Quit-':
            raise SystemExit

        # Opens the selected RDP file
        elif event == '-Button_Open-':
            x = value['demolist']
            filename = connectionDirectory + x[0] + ".rdp"
            powershellRun(filename)

        # Saves RDP variables entered to an RDP file
        elif event == '-newRDP_Button_Save-':
            if value['-newSettings_fullscreenInput-']:
                multi = "use multimon:i:1\n"
            else:
                multi = "\n"
            try:
                filename = "connections/" + value['-newRDP_NameInput-'] + ".rdp"
            except:
                print("We need a filename!")
                filename = "connections/dumbass.rdp"
            try:
                ip = hostentry + value['-newRDP_IPInput-'] + "\n"
            except:
                print("An IP address would be helpful, you know.")
                ip = "\n"
            try:
                user = userentry + value['-newRDP_UserInput-'] + "\n"
            except:
                user = "\n"
            try:
                password = passentry + encryptPassword(value['-newRDP_PassInput-']) + "\n"
            except:
                password = "\n"
            try:
                filecontents = multi + ip + user + password
            except:
                print("Failed to generate file contents")
                try:
                    print(multi)
                    print(ip)
                    print(user)
                    print(password)
                except:
                    pass
            try:
                createRDP(filename, filecontents)
            except Exception as e:
                print(e)
            x = getFiles()
            window['demolist'].update(values=x)


main()
