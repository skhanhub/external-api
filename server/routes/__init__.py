from flask import Flask

app = Flask(
  __name__,
  static_url_path='', 
  static_folder='../static',
)

from .api import movieDetails
from .api import movieNames
from routes import index


