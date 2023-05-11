import os
import urllib.request
from flask import Flask, request, redirect, jsonify, json
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/var/www/skol/uploads'

app = Flask(__name__)
app.secret_key = 'secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024

ALLOWED_EXTENSION = set(['txt', 'xml'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello():
    return redirect("/skol")

@app.route('/skol')
def skol():
    return "SKOL!"

@app.route('/skol/upload', methods=['GET','POST','PUT'])
def upload_file():
    if request.method == 'PUT':
        if request.data == b'':
            resp = jsonify({'response':{'message':'The file had no content'}})
            resp.status_code = 400
            return resp
        else:
            if 'fileName' not in request.args:
                resp = jsonify({'response':{'message': 'fileName is a required paramaeter'}})
                resp.status_code = 400
                return resp
            if request.args['fileName'] == '':
                resp = jsonify({'response': {'message': 'fileName cannot be blank'}})
                resp.status_code = 400
                return resp
            else:
                fileName = secure_filename(request.args['fileName'])
                filePath = os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(request.args['fileName']))
                if os.path.exists(filePath):
                    if 'overWrite' not in request.args and 'append' not in request.args:
                        resp = jsonify({'response':{'message':'That file has already been uploaded. Specify overWrite or append.'}})
                        resp.status_code = 200
                        return resp
                    if 'append' in request.args:
                        with open(filePath,'ab') as put_file:
                            put_file.write(request.data)
                        resp = jsonify({'response':[{'message': 'SKOL!'},{'fileName': fileName}]})
                        resp.status_code = 200
                        return resp
                    if 'overWrite' in request.args:
                        with open(filePath, 'wb') as put_file:
                            put_file.write(request.data)
                        resp = jsonify({'response':[{'message': 'SKOL!'},{'fileName': fileName}]})
                        resp.status_code = 200
                        return resp
                else:
                    with open(filePath, 'wb') as put_file:
                        put_file.write(request.data)
                    resp = jsonify({'response':[{'message': 'SKOL!'},{'fileName': fileName}]})
                    resp.status_code = 200
                    return resp
    if request.method == 'POST':
        if 'file' not in request.files:
            resp = jsonify({'response':{'message' : 'No file part in the request'}})
            resp.status_code = 400
            return resp
        
        if file.filename == '':
            resp = jsonify({'response':{'message' : 'No file selected for uploading'}})
            resp.status_code = 400
            return resp

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            resp = jsonify({'response':{'message': 'File sucessfully uploaded'}})
            resp.status_code = 201
            return resp
        
        else:
            resp = jsonify({'response':{'message': 'Unallowed File type'}})
            resp.status_code = 400
            return resp
        
    if request.method == 'GET':
        resp = jsonify({'response':{'message': 'Well go on then'}})
        resp.status_code = 200
        return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
