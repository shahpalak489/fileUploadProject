import os
import pandas as pd
from datetime import datetime
from time import time, strftime
from pytz import timezone
from app import config
from app import engine, connection
from flask import Blueprint, Flask, render_template, request, redirect, url_for, jsonify
misc_blueprint = Blueprint('misc_blueprint', __name__)
from werkzeug.utils import secure_filename

@misc_blueprint.route("/misc")
def cMisc():
   return render_template('home_v2.html')

@misc_blueprint.route("/file_upload")
def cMisc1():
   return render_template('file_upload.html')

UPLOAD_FOLDER = os.environ["FILE_UPLOAD_FLDER"]
ALLOWED_EXTENSIONS = {'txt', 'csv'}
def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@misc_blueprint.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      fileitem = request.files['file']
      if fileitem and allowed_file(fileitem.filename):
         filename = secure_filename(fileitem.filename)
         path = os.path.join(UPLOAD_FOLDER, filename)
         fileitem.save(path)

         ### load file into database
         df = pd.read_csv(path)  
         df = df.dropna(how='all')
         df["f_name"] = filename
         df["runid"] = int(datetime.now(timezone('US/Eastern')).strftime('%Y%m%d%H%M%S'))
         df["inserted_by"] = os.environ['USERNAME']
         df.to_sql("company_info_v2", connection, if_exists='append', index=False)
      # else:
      #    msg = "file format not allowed"
      #    return jsonify(success=True, data=msg)
      return redirect(url_for('misc_blueprint.upload_file'))
   return jsonify(success=True, data='file uploaded successfully')

@misc_blueprint.route("/fetch", methods = ['GET'])
def c_fetch():
   file = 'app/misc/sql/get_company_info.sql'
   f = open(file, 'r')
   df = pd.read_sql_query(f.read(), connection)
   return jsonify(success=True, data=df.to_dict(orient='records'))
