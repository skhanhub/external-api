from flask import Flask

app = Flask(__name__)

from .api import movieDetails
from .api import movieNames