from flask import Flask
 
app = Flask(__name__)

#register view functions
from .src.routes import main
app.register_blueprint(main)