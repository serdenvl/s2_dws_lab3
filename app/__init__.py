import os
from flask import Flask
from app_config import Config

app = Flask(__name__)
app.config.from_object(Config)

os.chdir(os.path.dirname(__file__))

from app import routes
