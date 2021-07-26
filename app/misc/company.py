import os
import pandas as pd
from datetime import datetime
from time import time, strftime
from pytz import timezone
from app import config
from app import engine, connection
from flask import Blueprint, Flask, request, redirect, url_for, jsonify
com_blueprint = Blueprint('com_blueprint', __name__)
import logging
logging.getLogger().setLevel(logging.DEBUG)
import traceback

def get_existed_comapny():
   file = 'app/misc/sql/get_unique_cid_cname.sql'
   f = open(file, 'r')
   df = pd.read_sql_query(f.read(), connection)
   return df

@com_blueprint.route("/company/list/v1", methods = ['GET', 'PUT'])
def c_add_combination():
   if request.method == 'GET':
      logging.info("-")
      logging.info(request.path + "...[" + request.method + "]")
      try:
         df = get_existed_comapny()
      except Exception as e:
         msg = "oops!! something went wrong, Please contact to team."
         logging.info("error: {}".format(e))
         traceback.print_exc()
         return jsonify(success=False, data=msg)
      return jsonify(success=True, data=df.to_dict(orient='records'))

   if request.method == 'PUT':
      logging.info("-")
      logging.info(request.path + "...[" + request.method + "]")
      res = request.get_json()['data']
      logging.info("user reqs: {}".format(res))
      try:
         ### check if company id, name is already existed
         df_existed = get_existed_comapny()
         df1 = df_existed[(df_existed['cid'] == int(res['c_id'])) | (df_existed['cname'] == res['c_name'])]
         if df1.empty == False:
            msg = "oops!! company list already existed."
            logging.info("check 1a: {}".format(msg))
            return jsonify(success=False, data=msg)
         
         ### add new company to database
         df = pd.DataFrame({'cid': [res['c_id']], 'cname': [res['c_name']], 'share_price_dt': [''], 
                           'share_price': [0.00], 'comments': ['new entry']})
         df.to_sql("company_info", connection, if_exists='append', index=False)
         msg = "yay!! successfully new company inserted."
         logging.info("success: {}".format(msg))
      except Exception as e:
         msg = "oops!! something went wrong, Please contact to team."
         logging.info("error: {}".format(e))
         traceback.print_exc()
         return jsonify(success=False, data=msg)
      return jsonify(success=True, data=msg)
