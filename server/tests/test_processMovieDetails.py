import unittest
import os
import requests
from unittest.mock import patch
from services.processMovieDetails import ProcessMovieDetails


returnData = {
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

    elif args[0] == 'http://webjetapitest.azurewebsites.net/api/filmworld/movie/fw0076759':
      return MockResponse(returnData, 200)


    return MockResponse(None, 404)

class TestProcessMovieDetailsClass(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    print('TestProcessMovieDetailsClass')

  def setUp(self):
    self.processMovieDetails = ProcessMovieDetails()
    self.processMovieDetails.setAccessToken(os.getenv('ACCESS_TOKEN'))
    self.processMovieDetails.setBaseURL('http://webjetapitest.azurewebsites.net')
    self.processMovieDetails.setCinemas(['filmworld'])

  def test_shouldReturnACodeOf2(self):
    print('should return a code of 2')
    with patch('services.processMovieNames.Session.get', side_effect=mocked_requests_get) as mocked_get:
      # Arrange
      self.processMovieDetails.setTimeout(1)
      # Act
      result = self.processMovieDetails.generateMovieDetails({"filmworld": "fw0076759"})
      # Assert
      self.assertEqual(result['code'], 2)
      mocked_get.assert_called_once

  def test_shouldReturnACodeOf0(self):
    print('should return the movie details with a code of 0')
    with patch('services.processMovieNames.Session.get', side_effect=mocked_requests_get) as mocked_get:
      # Arrange
      self.processMovieDetails.setTimeout(3)
      # Act
      result = self.processMovieDetails.generateMovieDetails({"filmworld": "fw0076759"})
      # Assert
      self.assertEqual(result['code'], 0)
      self.assertEqual(result['cinemas'],{
        "filmworld": {
            "Price": "29.5"
        }
      })
      mocked_get.assert_called_once

  def test_shouldReturnACodeOf1(self):
    print('should return a code of 1 and the movie details')
    # Arrange
    with patch('services.processMovieNames.Session.get', side_effect=mocked_requests_get) as mocked_get:
      self.processMovieDetails.setTimeout(3)
      self.processMovieDetails.generateMovieDetails({"filmworld": "fw0076759"})
    with patch('services.processMovieNames.Session.get', side_effect=mocked_requests_get) as mocked_get:
      self.processMovieDetails.setTimeout(1)

      # Act
      result = self.processMovieDetails.generateMovieDetails({"filmworld": "fw0076759"})
      # Assert
      self.assertEqual(result['code'], 1)
      self.assertEqual(result['cinemas'], {
        "filmworld": {
            "Price": "29.5"
        }
      })
      mocked_get.assert_called_once

if __name__ == '__main__':
    unittest.main()