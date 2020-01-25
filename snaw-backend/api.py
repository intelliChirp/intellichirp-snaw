from flask import Flask, render_template, send_file, jsonify
from flask import Flask, flash, request, redirect, url_for, session, render_template, jsonify, make_response
from werkzeug.utils import secure_filename
import os
import sys
import subprocess
from get_spectrogram import runScript as get_spectrogram
from classification import runScript as get_classification
from acousticIndices import getAcousticIndices as get_acoustic_indices
UPLOAD_FOLDER = 'instance/upload/'
ALLOWED_EXTENSIONS = {'wav'}

app = Flask("__main__")
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'secret key'
app.config['SESSION_TYPE'] = 'filesystem'

'''
App Routing: '/'
Function: home()
###------------------------------------------------------###
just renders the index.html file for react.
###------------------------------------------------------###
'''
@app.route('/')
def home():
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''
App Routing: '/uploader'
Function: upload_file()
Caller: App.js
###------------------------------------------------------###
handles the upload process. receives the files from App.js
and saves the files one at a time to the folder 'instance/upload'
###------------------------------------------------------###
'''
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
        # Request.Files comes in a immutable multi-dictionary.
        # MutableList uses a method to convert the imm. multi-dict to a mutable list.
        mutableList = request.files.copy()

        # iterate over a list received from getlist() method provided in mutableList's methodss
        for f in mutableList.getlist('file'):
            # Follow the same procedure as uploading singular files.
            filename = secure_filename(f.filename)
            f.save(os.path.join(UPLOAD_FOLDER, filename))
        return redirect('http://127.0.0.1:5000')


'''
App Routing: '/didUpload'
Function: didFileUpload()
Caller: Results.js
###------------------------------------------------------###
Checks to see if the folder 'instance/upload' has any contents
within in. returns a string 'True' or 'False' depending on the
condition.
###------------------------------------------------------###
'''
@app.route('/didUpload', methods = ['GET'])
def didFileUpload():
     # Create 'instance/upload/' folder if not present
    if(os.path.isdir('instance/upload/') == False):
        os.makedirs('instance/upload/')

    # Check if upload folder contains any files
    if(len(os.listdir('instance/upload/')) != 0):
        return "True"
    else:
        return "False"

'''
App Routing: '/results/classification'
Function: classify()
Caller: Results.js
###------------------------------------------------------###
calls the function runScript() within classification.py.
The fucntion runScript() is pulled into api.py as "get_classification()."
After the function finishes operations, the uploaded files will
be deleted.
###------------------------------------------------------###
'''
@app.route("/results/classification")
def classify():
    try:
        result = get_classification()

        for file in os.listdir('instance/upload/'):
            os.remove('instance/upload/'+file)

        return result
    except Exception as e:
        return str(e)

'''
App Routing: '/results/spectro'
Function: get_spectro()
Caller: Results.js
###------------------------------------------------------###
calls the function runScript() within get_spectrogram.py.
The function runScript() is pulled into api.py as "get_spectrogram()."
After the function finishes operations, the uploaded files will
be deleted.
###------------------------------------------------------###
'''v
@app.route("/results/spectro")
def get_spectro():
    try:
        result = get_spectrogram()
        return result
    except Exception as e:
        return str(e)

print('Starting Flask!')
app.run(debug=True)