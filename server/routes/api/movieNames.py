from routes import app
import os
from flask import jsonify, request
from services.processMovieNames import ProcessMovieNames
from config import getConfig

config = getConfig()

processMovieNames = ProcessMovieNames()
processMovieNames.setAccessToken(os.getenv('ACCESS_TOKEN'))
processMovieNames.setBaseURL(config['baseURL'])
processMovieNames.setCinemas(config['cinemaList'])
processMovieNames.setTimeout(config['timeout'])

@app.route("/api/movies", methods=['GET'])
def movies():
    if request.method == 'GET':
        return jsonify(processMovieNames.generateMovieList())