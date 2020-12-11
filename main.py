from ext_GUI import *


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
            filename = "connections/" + x[0] + ".rdp"
            powershellRun(filename)

        elif event == 'demolist':
            try:
                x = value['demolist']
                response = parseRDP(x[0])
                IP = response[0]
                User = response[1]
                window.Element('-display_Hostname_return-').Update(value=IP)
                window.Element('-display_User_return-').Update(value=User)
            except Exception as e:
                print(e)

        elif event == '-Button_Delete-':
            x = value['demolist']
            filename = connectionDirectory + x[0] + ".rdp"
            command = "del " + filename
            powershellRun(command)
            x = getFiles()
            window['demolist'].update(values=x)

        elif event == '-Button_Cheat-':
            window['-newRDP_NameInput-'].update(value="Test")
            window['-newRDP_IPInput-'].update(value="172.16.8.254")
            window['-newRDP_UserInput-'].update(value="Administrator")
            window['-newRDP_PassInput-'].update(value="Fuckyou")

        # Saves RDP variables entered to an RDP file
        elif event == '-newRDP_Button_Save-':
            # Try setting the filename
            if len(value['-newRDP_NameInput-']) < 2:
                print("We need a filename!")
                filename = "connections/whoops.rdp"
            else:
                filename = "connections/" + value['-newRDP_NameInput-'] + ".rdp"

            # Try setting the IP address
            try:
                ip = hostentry + value['-newRDP_IPInput-'] + "\n"
                filecontents = ip
            except:
                print("Missing IP address")

            # Try setting the Username
            try:
                user = userentry + value['-newRDP_UserInput-'] + "\n"
                filecontents = filecontents + user
            except:
                print("Missing username")

            # Try setting the password
            try:
                password = passentry + encryptPassword(value['-newRDP_PassInput-']) + "\n"
                filecontents = filecontents + password
            except:
                print("Missing password")

            # Catch if multimon is checked
            if value['-newSettings_fullscreenInput-']:
                multi = "use multimon:i:1\n"
                filecontents = filecontents + multi

            # Catch if "sign RDP file" is checked
            if value['-newSettings_signInput-']:
                sign = "sign"
            else:
                sign = "no"

            # Assemble the RDP file
            try:
                createRDP(filename, filecontents, sign)
            except Exception as e:
                print(e)

            # Update the RDP connection list
            x = getFiles()
            window['demolist'].update(values=x)


main()
