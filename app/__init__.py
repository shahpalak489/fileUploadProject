import os
from app import config
import sqlalchemy
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine('mssql+pyodbc://'+ 
                     os.environ["DB_SERVER"] + '/' + 
                     os.environ["DB_NAME"] + '?driver=' + 
                     os.environ["DB_DRIVER"])
connection = engine.connect()
session = sessionmaker(engine)    

# import pyodbc 
# conn = pyodbc.connect('Driver={SQL Server};'
#                      'Server=LAPTOP-QDH3PMIF;'
#                      'Database=master;'
#                      'Trusted_Connection=yes;')
# cursor = conn.cursor()
