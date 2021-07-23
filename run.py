import os
from flask import Flask
from app.misc.views import misc_blueprint

TEMPLATE_DIR = os.path.abspath('app/templates')
app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.register_blueprint(misc_blueprint)

@app.route("/")
def welcome():
    return "Welcome to File upload!"

if __name__ == "__main__":
    app.run(debug=True, port=5005)
    