import os
import pandas as pd
from datetime import datetime
from time import time, strftime
from pytz import timezone
from app import config
from app import engine, connection
from flask import Blueprint, Flask, request, redirect, url_for, jsonify
misc_blueprint = Blueprint('misc_blueprint', __name__)
from werkzeug.utils import secure_filename
from app.misc.company import get_existed_comapny
import logging
logging.getLogger().setLevel(logging.DEBUG)

UPLOAD_FOLDER = os.environ["FILE_UPLOAD_FLDER"]
ALLOWED_EXTENSIONS = {'txt', 'csv'}
def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@misc_blueprint.route('/file/uploader', methods = ['GET', 'POST'])
def c_file_uploader():
   if request.method == 'POST':
      logging.info("-")
      logging.info(request.path + "...[" + request.method + "]")

      fileitem = request.files['file']
      if fileitem and allowed_file(fileitem.filename):
         filename = secure_filename(fileitem.filename)
         path = os.path.join(UPLOAD_FOLDER, filename)
         fileitem.save(path)
         logging.info("Uploaded File location: {}".format(path))

         ### read csv/txt file
         df = pd.read_csv(path)  
         df = df.dropna(how='all')

         ### check for existing company list
         df_existed = get_existed_comapny()
         df_existed['combine'] = df_existed['cid'].astype(str) + df_existed['cname']
         df['combine'] = (df['cid'].astype(int)).astype(str) + df['cname']
         check =  all(item in df_existed['combine'].tolist() for item in df['combine'].tolist())
         if (check == False):
            msg = "oops!! company NA in database."
            logging.info("check 1: {}".format(msg))
            return jsonify(success=False, data=msg)
         df.drop(columns=['combine'], inplace=True)
         
         ### check for unique rows in df
         df2 = df[(df.duplicated('cid')) | (df.duplicated('cname'))]
         if df2.empty == False:
            msg = "oops!! duplicate entry in excel."
            logging.info("check 2: {}".format(msg))
            return jsonify(success=False, data=msg)

         ### check row count in excel file
         row_count = df.shape[0]
         if row_count < 5:
            msg = "oops!! minimum 5 rows required in excel."
            logging.info("check 3: {}".format(msg))
            return jsonify(success=False, data=msg)

         ### check comments size in excel
         mask = (df['comments'].str.len() > 256)
         df1 = df.loc[mask]
         if (df1.shape[0] > 0):
            msg = "oops!! comments > 256."
            logging.info("check 4: {}".format(msg))
            return jsonify(success=False, data=msg)

         ### load file into database
         logging.info("all check passed, ready to insert into databse")
         df["f_name"] = filename
         df["runid"] = int(datetime.now(timezone('US/Eastern')).strftime('%Y%m%d%H%M%S'))
         df["inserted_by"] = os.environ['USERNAME']
         df.to_sql("company_info_v2", connection, if_exists='append', index=False)
         msg = "successfully {} rows uploaded.".format(df.shape[0])
         logging.info("success: {}".format(msg))
      else:
         msg = "file format not allowed"
         logging.info("check 5: {}".format(msg))
         return jsonify(success=False, data=msg)
      # return redirect(url_for('misc_blueprint.upload_file'))
   return jsonify(success=True, data=msg)

@misc_blueprint.route("/fetch/uploaded/companies/v1", methods = ['GET'])
def c_fetch_uploaded_companies():
   logging.info("-")
   logging.info(request.path + "...[" + request.method + "]")
   file = 'app/misc/sql/get_company_info.sql'
   f = open(file, 'r')
   df = pd.read_sql_query(f.read(), connection)
   return jsonify(success=True, data=df.to_dict(orient='records'))
