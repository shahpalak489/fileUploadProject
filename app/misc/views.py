import os
import pandas as pd
import numpy as np
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
import traceback

UPLOAD_FOLDER = os.environ["FILE_UPLOAD_FLDER"]
ALLOWED_EXTENSIONS = {'txt', 'csv'}
def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_company_detail():
   file = 'app/misc/sql/get_company_info.sql'
   f = open(file, 'r')
   df = pd.read_sql_query(f.read(), connection)
   return df

@misc_blueprint.route('/file/uploader', methods = ['GET', 'POST'])
def c_file_uploader():
   if request.method == 'POST':
      logging.info("-")
      logging.info(request.path + "...[" + request.method + "]")
      try:
         fileitem = request.files['file']
         if not fileitem:
            msg = "please choose a file to upload."
            logging.info("check 1: {}".format(msg))
            return jsonify(success=False, data=msg)

         if not allowed_file(fileitem.filename):
            msg = "file format is not valid."
            logging.info("check 2: {}".format(msg))
            return jsonify(success=False, data=msg)

         filename = secure_filename(fileitem.filename)
         path = os.path.join(UPLOAD_FOLDER, filename)
         fileitem.save(path)
         logging.info("Uploaded File location: {}".format(path))

         ### read csv/txt file
         df = pd.read_csv(path)  
         df = df.dropna(how='all')

         ### check row count in excel file
         row_count = df.shape[0]
         if row_count < 5:
            msg = "minimum 5 rows required in excel."
            logging.info("check 3: {}".format(msg))
            return jsonify(success=False, data=msg)

         ### check cols in upload file
         required_cols = ['cid', 'cname', 'share_price_dt', 'share_price', 'comments']
         available_cols = list(df)
         if required_cols != available_cols:
            msg = "missing or extra columns in excel."
            logging.info("check 4: {}".format(msg))
            return jsonify(success=False, data=msg)

         ### check for existing company list
         df_existed = get_existed_comapny()
         df_existed['combine'] = df_existed['cid'].astype(str) + df_existed['cname']
         df['combine'] = (df['cid'].astype(int)).astype(str) + df['cname']
         check =  all(item in df_existed['combine'].tolist() for item in df['combine'].tolist())
         if (check == False):
            msg = "company not available in database."
            logging.info("check 5: {}".format(msg))
            return jsonify(success=False, data=msg)
         df.drop(columns=['combine'], inplace=True)
            
         ### check for unique rows in df
         df_duplicated = df[(df.duplicated('cid')) | (df.duplicated('cname'))]
         if df_duplicated.empty == False:
            msg = "duplicate entry in excel."
            logging.info("check 6: {}".format(msg))
            return jsonify(success=False, data=msg)

         ### check comments size in excel
         mask = (df['comments'].str.len() > 256)
         df_size = df.loc[mask]
         if (df_size.shape[0] > 0):
            msg = "comments should be less than 256 chars."
            logging.info("check 7: {}".format(msg))
            return jsonify(success=False, data=msg)
         
         ### check share price limitation
         df_detail = get_company_detail()
         df_detail.drop(columns=['share_price_dt', 'comments', 'f_name'], inplace=True)
         df_merged = pd.merge(df_detail, df, how='left', on=['cid','cname'])
         df_merged['check_share_price'] = df_merged['share_price_x'] * 10
         if (df_merged['check_share_price'] <= df_merged['share_price_y']).any():
            msg = "share price is 10 times more than prev entry."
            logging.info("check 8: {}".format(msg))
            return jsonify(success=False, data=msg)

         ### load file into database
         logging.info("Yay!! all checks passed, ready to insert into databse")
         df["f_name"] = filename
         df["runid"] = int(datetime.now(timezone('US/Eastern')).strftime('%Y%m%d%H%M%S'))
         df["inserted_by"] = os.environ['USERNAME']
         df['share_price_dt']= pd.to_datetime(df['share_price_dt'], errors='coerce')
         df.to_sql("company_info", connection, if_exists='append', index=False)
         msg = "successfully {} rows uploaded.".format(df.shape[0])
         logging.info("success: {}".format(msg))
      except Exception as e:
         msg = "oops!! something went wrong, Please contact to team."
         logging.info("error: {}".format(e))
         traceback.print_exc()
         return jsonify(success=False, data=msg)
      # return redirect(url_for('misc_blueprint.upload_file'))
   return jsonify(success=True, data=msg)

@misc_blueprint.route("/fetch/uploaded/companies/v1", methods = ['GET'])
def c_fetch_uploaded_companies():
   logging.info("-")
   logging.info(request.path + "...[" + request.method + "]")
   try:
      df = get_company_detail()
   except Exception as e:
      msg = "oops!! something went wrong, Please contact to team."
      logging.info("error: {}".format(e))
      traceback.print_exc()
      return jsonify(success=False, data=msg)
   return jsonify(success=True, data=df.to_dict(orient='records'))
