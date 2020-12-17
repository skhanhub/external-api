import unittest
import json
import ast
import requests
from unittest.mock import patch
from routes import app

moviesData = {
  "Movies": [
      {
          "Title": "Star Wars: Episode IV - A New Hope",
          "Year": "1977",
          "ID": "fw0076759",
          "Type": "movie",
          "Poster": "http://ia.media-imdb.com/images/M/MV5BOTIyMDY2NGQtOGJjNi00OTk4LWFhMDgtYmE3M2NiYzM0YTVmXkEyXkFqcGdeQXVyNTU1NTfwOTk@._V1_SX300.jpg"
      }

  ]
}

detailsData = {
  "Title": "Star Wars: Episode IV - A New Hope",
  "Year": "1977",
  "Rated": "PG",
  "Released": "25 May 1977",
  "Runtime": "121 min",
  "Genre": "Action, Adventure, Fantasy",
  "Director": "George Lucas",
  "Writer": "George Lucas",
  "Actors": "Mark Hamill, Harrison Ford, Carrie Fisher, Peter Cushing",
  "Plot": "Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a wookiee and two droids to save the galaxy from the Empire's world-destroying battle-station, while also attempting to rescue Princess Leia from the evil Darth Vader.",
  "Language": "English",
  "Country": "USA",
  "Poster": "http://ia.media-imdb.com/images/M/MV5BOTIyMDY2NGQtOGJjNi00OTk4LWFhMDgtYmE3M2NiYzM0YTVmXkEyXkFqcGdeQXVyNTU1NTfwOTk@._V1_SX300.jpg",
  "Metascore": "92",
  "Rating": "8.7",
  "Votes": "915,459",
  "ID": "fw0076759",
  "Type": "movie",
  "Price": "29.5"
}
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
          self.json_data = json_data
          self.status_code = status_code

        def json(self):
          return self.json_data

    
    if kwargs['timeout']<2:
      raise requests.exceptions.HTTPError('timeout')

    elif args[0] == 'http://webjetapitest.azurewebsites.net/api/filmworld/movies':
      return MockResponse(moviesData, 200)

    elif args[0] == 'http://webjetapitest.azurewebsites.net/api/filmworld/movie/fw0076759':
      return MockResponse(detailsData, 200)


    return MockResponse(None, 404)

class TestRoutes(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    print('TestRoutes')



  def test_404(self):
    print('should return a status_code of 404')
    with patch('services.processMovieNames.Session.get', side_effect=mocked_requests_get) as mocked_get:
      # Arrange
      client = app.test_client(self)
      # Act
      response = client.get('/api/random')
      # Assert
      self.assertEqual(response.status_code, 404)

  def test_movieRoute(self):
    print('should return a status_code of 200')
    with patch('services.processMovieNames.Session.get', side_effect=mocked_requests_get) as mocked_get:
      # Arrange
      client = app.test_client(self)
      # Act
      response = client.post(
        '/api/movie',
        data=json.dumps({"filmworld": "fw0076759"}),
        content_type='application/json')
      data = ast.literal_eval(response.data.decode("UTF-8"))
      # Assert
      self.assertEqual(response.status_code, 200)
      self.assertEqual(data['code'], 0)
      self.assertEqual(data['cinemas'], {
        "filmworld": {
            "Price": "29.5"
        }
      })
      mocked_get.assert_called_once


if __name__ == '__main__':
    unittest.main()