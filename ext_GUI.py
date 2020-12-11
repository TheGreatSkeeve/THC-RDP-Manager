from ext_functions import *

# GUI Stuff
Button_Open = sg.Button("Connect", key='-Button_Open-', bind_return_key=True)
Button_Delete = sg.Button("Delete", key='-Button_Delete-', bind_return_key=True)
Button_Quit = sg.Button("Quit", key='-Button_Quit-', bind_return_key=True)
Button_Cheat = sg.Button("Cheat", key='-Button_Cheat-', bind_return_key=True)
sg.theme('SystemDefault1')

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
newSettings_sign = sg.Text("Sign RDP file?")
newSettings_signInput = sg.CBox('', size=(10, 15), key="-newSettings_signInput-")

column_new = sg.Col([
    [newRDP_Text], [newRDP_Name, newRDP_NameInput], [newRDP_IP, newRDP_IPInput], [newRDP_User, newRDP_UserInput],
    [newRDP_Pass, newRDP_PassInput], [newSettings_fullscreen, newSettings_fullscreenInput],
    [newSettings_sign, newSettings_signInput], [newRDP_Button_Save, Button_Cheat]])

# Display Info about the RDP file
display_Title = sg.Text("Connection details:", size=(30, 1))
display_Hostname = sg.Text("Hostname / IP:")
display_User = sg.Text("Username:")
display_Pass = sg.Text("Password:")
display_Hostname_return = sg.Text(" ", key='-display_Hostname_return-', size=(30, 1))
display_User_return = sg.Text(" ", key='-display_User_return-', size=(30, 1))
display_Pass_return = sg.Text(" ", key='-display_Pass_return-', size=(30, 1))

column_display = sg.Col(
    [[display_Title], [display_Hostname, display_Hostname_return], [display_User, display_User_return],
     [display_Pass, display_Pass_return]], justification="top")

# Create and populate current RDP connection listbox
listbox_browse = sg.Listbox(values=currentlist, size=(30, 15), select_mode=sg.SELECT_MODE_EXTENDED, key='demolist',
                            bind_return_key=True, change_submits=True)
listbox_text = sg.Text("Saved Connections:", font='Helvetica 13', )

column_connections = sg.Col([[listbox_text], [listbox_browse], [Button_Open, Button_Delete]])

# Create the Dev console
devOutput = sg.Output(size=(175, 15), font='Helvetica 10', key='_output_', visible=True)
devOuputText = sg.Text("Console Output / Errors:")
column_dev = sg.Col([[devOuputText], [devOutput]])

# Define the GUI's layout
layout = [
    [column_connections, column_display, column_new],  #
    [column_dev]
]

# Create the GUI
window = sg.Window(
    'THC RDP Manager', layout,
    default_element_size=(30, 2), resizable=True,
    font=('Helvetica', ' 13'),
    icon='icon.ico',
    default_button_element_size=(4, 1),
    return_keyboard_events=True
)
