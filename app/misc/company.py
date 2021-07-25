import os
import pandas as pd
from datetime import datetime
from time import time, strftime
from pytz import timezone
from app import config
from app import engine, connection
from flask import Blueprint, Flask, render_template, request, redirect, url_for, jsonify
com_blueprint = Blueprint('com_blueprint', __name__)

@com_blueprint.route("/company/list/v1", methods = ['GET', 'PUT'])
def c_add_combination():
   if request.method == 'GET':
      file = 'app/misc/sql/get_unique_cid_cname.sql'
      f = open(file, 'r')
      df = pd.read_sql_query(f.read(), connection)
      return jsonify(success=True, data=df.to_dict(orient='records'))

   if request.method == 'PUT':
      d = request.get_json()['data']
      df = pd.DataFrame({'cid': [d['c_id']], 'cname': [d['c_name']], 'share_price_dt': [''], 'share_price': [0.00], 'comments': ['new entry']})
      df.to_sql("company_info_v2", connection, if_exists='append', index=False)
      return jsonify(success=True, data="successfully company inserted")
