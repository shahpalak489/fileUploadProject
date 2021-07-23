from flask import Blueprint, Flask, render_template, request, redirect, url_for
misc_blueprint = Blueprint('misc_blueprint', __name__)
from werkzeug.utils import secure_filename
import os
import pandas as pd
from datetime import datetime
from time import time, strftime
from pytz import timezone

UPLOAD_FOLDER = 'app/data/'
ALLOWED_EXTENSIONS = {'txt', 'csv'}

@misc_blueprint.route("/misc")
def cMisc():
   return render_template('home.html')

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@misc_blueprint.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      # if 'file' not in request.files:
      #    flash('No file part')
      #    return redirect(request.url)
      fileitem = request.files['file']
      # if fileitem.filename == '':
      #    flash('No selected file')
      #    return redirect(request.url)
      if fileitem and allowed_file(fileitem.filename):
         filename = secure_filename(fileitem.filename)
         path = os.path.join(UPLOAD_FOLDER, filename)
         fileitem.save(path)

         ### load file into database
         df = pd.read_csv(path)  
         df["runid"] = int(datetime.now(timezone('US/Eastern')).strftime('%Y%m%d%H%M%S'))
         df["uploaded_by"] = 'pshah'
         print(df)

      else:
         msg = "file format not allowed"
         print(msg)
         return msg
      return redirect(url_for('misc_blueprint.upload_file'))
   return 'file uploaded successfully'

