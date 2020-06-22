from flask import Flask, flash, request, redirect, url_for, send_file, after_this_request
from werkzeug.utils import secure_filename
import os

from src.classifier import Regressor

UPLOAD_FOLDER = './uploaded/'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(64).hex()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(f'filename is {filename}')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_filename = ".queued_"+filename
            os.rename(os.path.join(app.config['UPLOAD_FOLDER'],filename), 
                      os.path.join(app.config['UPLOAD_FOLDER'],new_filename))
            saved_file = "out_"+new_filename[1:]
            @after_this_request
            def remove_files(response):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'],new_filename))
                os.remove(saved_file)
                return response
            clf.predict(os.path.join(app.config['UPLOAD_FOLDER'], new_filename)).to_excel(saved_file)
            return send_file(saved_file)
            #return f'Saved successfully as {new_filename}!'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    clf = Regressor(saved_model='saved_model/model.cfg')
    app.run(host='0.0.0.0',port='5000',debug=True)