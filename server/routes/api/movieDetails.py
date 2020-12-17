from routes import app
import os
from flask import jsonify, request
from services.processMovieDetails import ProcessMovieDetails
from config import getConfig

config = getConfig()

processMovieDetails = ProcessMovieDetails()
processMovieDetails.setAccessToken(os.getenv('ACCESS_TOKEN'))
processMovieDetails.setBaseURL(config['baseURL'])
processMovieDetails.setCinemas(config['cinemaList'])
processMovieDetails.setTimeout(config['timeout'])

@app.route("/api/movie", methods=['POST'])
def movie():
    if request.method == 'POST':
        return jsonify(processMovieDetails.generateMovieDetails(request.json))