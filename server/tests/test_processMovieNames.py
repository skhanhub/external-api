import unittest
import os
import requests
from unittest.mock import patch
from services.processMovieNames import ProcessMovieNames


returnData = {
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
      return MockResponse(returnData, 200)


    return MockResponse(None, 404)

class TestProcessMovieNamesClass(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    print('TestProcessMovieNamesClass')

  def setUp(self):
    self.processMovieNames = ProcessMovieNames()
    self.processMovieNames.setAccessToken(os.getenv('ACCESS_TOKEN'))
    self.processMovieNames.setBaseURL('http://webjetapitest.azurewebsites.net')
    self.processMovieNames.setCinemas(['filmworld'])

  def test_shouldReturnACodeOf2(self):
    print('should return a code of 2')
    with patch('services.processMovieNames.Session.get', side_effect=mocked_requests_get) as mocked_get:
      # Arrange
      self.processMovieNames.setTimeout(1)
      # Act
      result = self.processMovieNames.generateMovieList()
      # Assert
      self.assertEqual(result['code'], 2)
      mocked_get.assert_called_once

  def test_shouldReturnACodeOf0(self):
    print('should return the available movies for filmworld with a code of 0')
    with patch('services.processMovieNames.Session.get', side_effect=mocked_requests_get) as mocked_get:
      # Arrange
      self.processMovieNames.setTimeout(3)
      # Act
      result = self.processMovieNames.generateMovieList()
      # Assert
      self.assertEqual(result['code'], 0)
      self.assertEqual(result['movies'], {
        "Star Wars: Episode IV - A New Hope": {
            "filmworld": "fw0076759"
        }
      })
      mocked_get.assert_called_once

  def test_shouldReturnACodeOf1(self):
    print('should return a code of 1 and the the available movies')
    # Arrange
    with patch('services.processMovieNames.Session.get', side_effect=mocked_requests_get) as mocked_get:
      self.processMovieNames.setTimeout(3)
      self.processMovieNames.generateMovieList()
    with patch('services.processMovieNames.Session.get', side_effect=mocked_requests_get) as mocked_get:
      self.processMovieNames.setTimeout(1)

      # Act
      result = self.processMovieNames.generateMovieList()
      # Assert
      self.assertEqual(result['code'], 1)
      self.assertEqual(result['movies'], {
        "Star Wars: Episode IV - A New Hope": {
            "filmworld": "fw0076759"
        }
      })
      mocked_get.assert_called_once

if __name__ == '__main__':
    unittest.main()