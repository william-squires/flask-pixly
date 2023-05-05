"""Flask app for Pixly"""
from flask import Flask, jsonify, request
from models import connect_db, db, Image
from flask_cors import CORS
from s3 import upload_file_to_s3
import base64
from random import sample

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

connect_db(app)

UPLOAD_FOLDER = 'static/uploads'
DOWNLOAD_FOLDER = 'static/downloads'
BASE_URL = os.environ.get('AWS_BUCKET_BASE_URL')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    ''' Checks to see if a file is of an acceptable type'''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_make(exifobj):
    ''' Gets make from exif data '''
    return exifobj.get("tags").get("Make")


def get_model(exifobj):
    '''Gets model from exif data'''
    return exifobj.get("tags").get("Model")


def get_file_extension(filename):
    ''' Gets file extension from filename '''
    return filename.split('.')[1].lower()


def get_base64_string(str):
    '''removes data about base 64 encoded string and returns
      just the encoded part.
      '''
    return str.split(',')[1]


@app.post('/')
def upload_file():
    '''
    uploadsfile to s3 and puts info about it in the database
    '''
    jpg_b64_string_data = get_base64_string(request.json.get("encodedImage"))
    name = request.json.get("name")
    image_data = base64.b64decode(jpg_b64_string_data)
    filename = f'{DOWNLOAD_FOLDER}/{name}'
    f = open(filename, "wb")
    f.write(image_data)
    f.close()
    make = get_make(request.json.get("exif"))
    model = get_model(request.json.get("exif"))
    description = request.json.get("description", "")
    try:
        object_name = upload_file_to_s3(filename)
    except Exception:
        print('An error is happening')
    image = Image(image_id=object_name,
                  filename=name,
                  file_extension=get_file_extension(filename),
                  make=make, model=model,
                  description=description)
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
    return jsonify(url=f'{BASE_URL}{img_id}')


@app.get('/')
def get_images():
    '''return json object of all image urls'''

    images = Image.query.all()
    urls = []
    for image in images:
        urls.append({"url": f'{BASE_URL}{image.image_id}'})
    return jsonify(urls)


@app.get('/search')
def get_images_by_search_term():
    """searches for an image by method and term"""
    term = request.args.get("term", "")
    method = request.args.get("method")
    if method == "description":
        images = Image.query.filter(Image.description.ilike(f'%{term}%')).all()
    elif method == "make":
        images = Image.query.filter(Image.make.ilike(f'%{term}%')).all()
    elif method == "model":
        images = Image.query.filter(Image.model.ilike(f'%{term}%')).all()

    urls = []
    for image in images:
        urls.append({"url": f'{BASE_URL}{image.image_id}'})
    return jsonify(urls)


@app.get('/random')
def get_random_images():
    """returns urls to random image. takes count query param to specify how many."""
    count = request.args.get("count", 1)

    images = Image.query.all()
    urls = []
    for image in images:
        urls.append({"url": f'{BASE_URL}{image.image_id}'})
    urls = sample(urls, int(count))
    return jsonify(urls)
