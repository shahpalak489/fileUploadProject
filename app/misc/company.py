import os
import pandas as pd
from datetime import datetime
from time import time, strftime
from pytz import timezone
from app import config
from app import engine
from flask import Blueprint, Flask, render_template, request, redirect, url_for, jsonify
com_blueprint = Blueprint('com_blueprint', __name__)

@com_blueprint.route("/com")
def c_com():
   return render_template('home_v2.html')

@com_blueprint.route("/get/existed/company/list/v1", methods = ['GET'])
def c_unique_combination():
   file = 'app/misc/sql/get_unique_cid_cname.sql'
   f = open(file, 'r')
   df = pd.read_sql_query(f.read(), engine.connect())
   return jsonify(success=True, data=df.to_dict(orient='records'))

