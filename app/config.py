import socket
import os
import getpass

os.environ['USERNAME'] = getpass.getuser()
os.environ['HOSTNAME'] = socket.gethostname()
os.environ["ENVIRONMENT"] = "DEV"
os.environ["DB_SERVER"] = "LAPTOP-QDH3PMIF"
os.environ["DB_NAME"] = "master"
os.environ["DB_USER"] = ""
os.environ["DB_PASSWORD"] = ""
os.environ["DB_DRIVER"] = "SQL+Server+Native+Client+11.0"
os.environ["TEMPLATE"] = 'app/templates'
os.environ["STATIC"] = 'app/static'
os.environ["FILE_UPLOAD_FLDER"] = 'app/data'
