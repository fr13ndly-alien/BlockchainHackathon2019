from flask import Flask
app = Flask(__name__)

from app import routes
UPLOAD_FOLDER = 'file_upload_location'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'secret_key'
# app.secret_key = "secret key"