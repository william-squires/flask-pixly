"""Flask app for Pixly"""
from flask import Flask, jsonify, request, render_template, redirect, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from models import connect_db, db, Image
from flask_cors import CORS
from s3 import upload_file_to_s3, download_file_from_s3

import os

OK_STATUS_CODE = 200
CREATE_STATUS_CODE = 201

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///pixly")

CORS(app)
debug = DebugToolbarExtension(app)

connect_db(app)

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    ''' Checks to see if a file is of an acceptable type'''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_extension(filename):
    ''' Gets file extension from filename '''
    return filename.split('.')[1].lower()


@app.post('/')
def upload_file():
    '''
    (TODO:) If invalid file will throw an error
    Otherwise removes whitespace from filename and saves it to uploads and
    uploads to s3
    Puts file in the database
    '''
    if 'file' not in request.files:
        return jsonify("no file")
    file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
    if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            try:
                object_name = upload_file_to_s3(f'uploads/{filename}')
            except Exception:
                print('An error is happening')
            image = Image(image_id=object_name, filename=filename,
                          file_extension=get_file_extension(filename))
            db.session.add(image)
            db.session.commit()
            return jsonify(uploaded="uploaded")


@app.get('/<image_id>')
def download_file(image_id):
    '''
    Gets image by id from API and downloads from s3
    Returns json about image
    '''
    file = Image.query.get_or_404(image_id)
    img_id = file.image_id
    extension = file.file_extension
    download_file_from_s3(img_id, extension)
    return jsonify(img_id)
