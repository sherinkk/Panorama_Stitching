import os
from werkzeug.utils import secure_filename
import subprocess
from flask import Flask,redirect,url_for,render_template,request,flash
from stit_final import *

i = 0
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)
app.secret_key="keerikadan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/team')
def team():
    return render_template('team.html')    


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    global i
    if request.method == 'POST':
        filenames=[]
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('files not selected')
            print("file non")
            return render_template('upload.html')
        files = request.files.getlist("file")
        print(files)
        # if len(files)<3:
        #     flash('No enough file')
        #     print("h3")
        #     return render_template('upload.html')

        for file in files:
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            print(file.filename)
            #file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('Not enough files selected')
                return render_template('upload.html')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filenames.append(filename)
            else:
                flash('Incorrect image format.....SUPPORTED FORMATS = {png, jpg, jpeg}')
                return render_template('upload.html')

        print(filenames)
        stitchdriver(filenames,"static/images/answer"+str(i)+".jpg")
        send_ = "answer"+str(i)+".jpg"
        i+=1


        return render_template('result.html',answer1='',answer2='',answer3='',send_=send_)
        

    else:
        return render_template('upload.html')
    return 


if __name__ == '__main__':
    app.run(debug=True)
