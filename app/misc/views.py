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

         ### read csv/txt file
         df = pd.read_csv(path)  
         df = df.dropna(how='all')

         ### check for unique rows in df
         # df2 = df[df.duplicated(['cid', 'cname'])]
         df2 = df[(df.duplicated('cid')) | (df.duplicated('cname'))]
         if df2.empty == False:
            return jsonify(success=False, data="oops!! duplicate entry in excel")

         ### check row count in excel file
         row_count = df.shape[0]
         if row_count < 5:
            msg = "minimum 5 rows required."
            return jsonify(success=False, data=msg)

         ### check comments size in excel
         mask = (df['comments'].str.len() > 256)
         df1 = df.loc[mask]
         if (df1.shape[0] > 0):
            print("here")
            msg = "Comments are > 255."
            return jsonify(success=False, data=msg)

         ### load file into database
         df["f_name"] = filename
         df["runid"] = int(datetime.now(timezone('US/Eastern')).strftime('%Y%m%d%H%M%S'))
         df["inserted_by"] = os.environ['USERNAME']
         df.to_sql("company_info_v2", connection, if_exists='append', index=False)
      else:
         msg = "file format not allowed"
         return jsonify(success=False, data=msg)
      # return redirect(url_for('misc_blueprint.upload_file'))
   return jsonify(success=True, data='file uploaded successfully')

@misc_blueprint.route("/fetch", methods = ['GET'])
def c_fetch():
   file = 'app/misc/sql/get_company_info.sql'
   f = open(file, 'r')
   df = pd.read_sql_query(f.read(), connection)
   return jsonify(success=True, data=df.to_dict(orient='records'))
