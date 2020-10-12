# GUI + CUI
# Version 1.1.4
import library.modules.bootstrap as bootstrap
import time
import argparse
import logging
import os
import library.modules.config as config

config.main()
parser = argparse.ArgumentParser(description='GUI / CUI')
parser.add_argument('-g', action="store_true", required=False)
parser.add_argument('-c', action="store_true", required=False)
args = parser.parse_args()
if args.g:
    config.interface = "GUI"
elif args.c:
    config.interface = "CUI"

if __name__ == '__main__':
    try:
        start = bootstrap.main()
        interface = config.interface
        if start:
            import library.commands.global_interface.clear as clear
            if interface == "CUI":
                import library.interfaces.home_interface as home_interface
                clear.main()
                home_interface.main()
            elif interface == "GUI":
                import library.interfaces.listener_interface as listener_interface
                import library.interfaces.generator_interface as generator_interface
                import library.interfaces.home_interface as home_interface
                import library.interfaces.scout_interface as scout_interface
                import library.interfaces.direct_interface as direct_interface
                import library.modules.monitor_listeners as monitor_listeners
                import library.modules.log as log
                from flask import Flask, redirect, url_for, send_from_directory, render_template, request, jsonify
                import sys
                clear.main()
    except EOFError:
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            print('[!]User aborted bootstrap, requesting shutdown...')
            quit()
    except KeyboardInterrupt:
        print('[!]User aborted bootstrap, requesting shutdown...')
        quit()
    except Exception as e:
        logging.critical("Critical Error occurred please inform developer, dumping stack trace and exiting...", exc_info=True)

try:
    app = Flask(__name__, static_folder="web_interface/static", template_folder="web_interface/templates")
    app.secret_key = os.urandom(24)
    config.app = app
    log.plaintext("PyIris Web Interface Started on \033[35mlocalhost\033[0m:\033[35m5000\033[0m")
except Exception as e:
    logging.critical("Critical Error occurred please inform developer, dumping stack trace and exiting...", exc_info=True)
    quit()


@app.route('/')
def redirect_from_root():
    return redirect(url_for('home'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'web_interface/static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/home', methods=['GET', 'POST'])
def home():
    config.abrupt_end = True
    log.page_loaded("Home")
    return render_template('home.html')


@app.route('/generator', methods=['GET', 'POST'])
def generator():
    config.abrupt_end = True
    log.page_loaded("Generator")
    return render_template('generator.html')


@app.route('/listeners', methods=['GET', 'POST'])
def listener():
    config.abrupt_end = True
    log.page_loaded("Listeners")
    return render_template('listeners.html')


@app.route('/scouts', methods=['GET', 'POST'])
def scouts():
    config.abrupt_end = True
    log.page_loaded("Scouts")
    return render_template('scouts.html')


"""
@app.route('/testing', methods=['GET', 'POST'])
def testing():
    config.abrupt_end = True
    log.page_loaded("Testing")
    return render_template('testing.html')
"""


@app.route('/home_process', methods=['GET', 'POST'])
def home_process():
    config.bridged = False
    config.bridged_to = None
    log.request_made(str(request.form['command']), "Home_Process")
    output = home_interface.main(request.form['command'])
    return output


@app.route('/generator_process', methods=['GET', 'POST'])
def generator_process():
    config.bridged = False
    config.bridged_to = None
    log.request_made(str(request.form['command']), "Generator_Process")
    output = generator_interface.main(request.form['command'])
    return output


@app.route('/listeners_process', methods=['GET', 'POST'])
def listener_process():
    log.request_made(str(request.form['command']), "Listeners_Process")
    if request.form['command'] is not None:
        config.bridged = False
        config.bridged_to = None
        output = listener_interface.main(request.form['command'])
        return output


@app.route('/scouts_process', methods=['GET', 'POST'])
def scouts_process():
    log.request_made(str(request.form['command']), "Scouts_Process")
    output = scout_interface.main(request.form['command'])
    return output


@app.route('/direct_process', methods=['GET', 'POST'])
def direct_process():
    log.request_made(str(request.form['command']), "Direct_Process")
    output = direct_interface.main(request.form['scoutId'], request.form['command'])
    if output == "return to scouts":
        output = jsonify({"output": "Success", "output_message": "Returning to scouts", "data": ""})
    return output


@app.route('/monitor_process', methods=['GET', 'POST'])
def monitor_process():
    log.request_made(str(request.form['command']), "Monitor_Process")
    if request.form['command'].split(' ')[0] == "monitor":
        if request.form['command'].split(' ')[1] == "normal":
            output = monitor_listeners.main()
        elif request.form['command'].split(' ')[1] == "reload":
            output = monitor_listeners.check()
        return output


if __name__ == '__main__' and interface == "GUI":
    app.run()
