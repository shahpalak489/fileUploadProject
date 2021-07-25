import os
from flask import Flask
from app.misc.views import misc_blueprint
from app.misc.company import com_blueprint
from app import config

TEMPLATE_DIR = os.path.abspath(os.environ["TEMPLATE"])
STATIC_DIR = os.path.abspath(os.environ["STATIC"])
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.register_blueprint(misc_blueprint)
app.register_blueprint(com_blueprint)

@app.route("/")
def welcome():
    return "Welcome to File upload!"

if __name__ == "__main__":
    app.run(debug=True, port=5005)
    