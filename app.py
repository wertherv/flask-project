import glob
import os

from flask import Flask, flash, redirect, abort, send_from_directory
from flask import render_template
from flask_cas import CAS
from flask import session
from flask import request
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
UPLOAD_FOLDER = './download/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CAS_SERVER'] = 'https://login.uph.edu.pl'
app.config['CAS_LOGIN_ROUTE'] = '/login'
app.config['CAS_AFTER_LOGIN'] = 'after_login'
app.config['CAS_VALIDATE_ROUTE'] = 'serviceValidate'
app.config['CAS_LOGOUT_ROUTE'] = '/logout'
# app.config['CAS_AFTER_LOGOUT'] = 'http://'
csrf = CSRFProtect()
CAS(app)
csrf.init_app(app)


@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    print(2)
    return render_template('main.html')


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'CAS_USERNAME' in session:
        if request.method == 'POST':
            f = request.files['filename']
            if f.filename == '':
                flash('Nie wybrano pliku')
                return redirect(request.url)

                # f.stream.close()
            files = glob.glob(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']) + '/*')
            for ff in files:
                try:
                    os.remove(ff)

                except OSError as e:
                    print("Error: %s : %s" % (ff, e.strerror))

            if process_file(f):
                print(1)
            return redirect('/')
        else:
            return redirect('/')
    else:
        abort(403)


@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    if 'CAS_USERNAME' in session:
        if filename == "":
            abort(404)
        full_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
        return send_from_directory(full_path, filename)
    else:
        abort(403)


def process_file(f):
    usos_file = b''
    irk_file = b''
    akademiki_file = b''
    l = ''
    # f.
    line = f.stream.readline()
    if line[0:15] == b'"01","UNIWERSYT':

        usos_file = line
        irk2_file = line
        akademiki_file = line
        usos_sum = 0
        irk_sum = 0
        akad_sum = 0
        usos_ile = 0
        irk_ile = 0
        akad_ile = 0
        orig_file = line

        while line:
            line = f.stream.readline()
            sl = line.split(b',')
            if sl[0] == b'"02"':
                if sl[6].decode()[1] == "1":
                    usos_sum = usos_sum + int(sl[3])
                    usos_file = usos_file + line
                    usos_ile = usos_ile + 1
                if sl[6].decode()[1] == "0":
                    irk_sum = irk_sum + int(sl[3])
                    irk_file = irk_file + line
                    irk_ile = irk_ile + 1
                if sl[6].decode()[1] == "2":
                    akad_sum = akad_sum + int(sl[3])
                    akademiki_file = akademiki_file + line
                    akad_ile = akad_ile + 1

            if sl[0] == b'"03"':
                usos_file = usos_file + b'"03",' + str(usos_ile).encode() + b',' + str(usos_sum).encode() + b'\r\n'
                irk_file = irk_file + b'"03",' + str(irk_ile).encode() + b',' + str(irk_sum).encode() + b'\r\n'
                akademiki_file = akademiki_file + b'"03,"' + str(akad_ile).encode() + b',' + str(
                    akad_sum).encode() + b'\r\n'
            orig_file = orig_file + line
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        session['files'] = []
        with open(app.config['UPLOAD_FOLDER'] + f.filename, "wb") as fu:
            fu.write(orig_file)
        print(usos_file)
        with open(app.config['UPLOAD_FOLDER'] + f.filename + "_U", "wb") as fu:
            fu.write(usos_file)
            session['files'].append(f.filename + "_U")
        print("!!!!!!!!!!")
        print(irk_file)
        with open(app.config['UPLOAD_FOLDER'] + f.filename + "_I", "wb") as fu:
            fu.write(irk_file)
            session['files'].append(f.filename + "_I")
        print("!!!!!!!!!!")
        print(akademiki_file)
        with open(app.config['UPLOAD_FOLDER'] + f.filename + "_A", "wb") as fu:
            fu.write(akademiki_file)
            session['files'].append(f.filename + "_A")
        print("!!!!!!!!!!")
        return 1
    else:
        return 0


@app.route('/after_login', methods=['GET'])
def after_login():
    print(1)

    return redirect('/')


@app.route('/logout', methods=['GET'])
def logout():
    print(2)

    return redirect('/')


# application = app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
