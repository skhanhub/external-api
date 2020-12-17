import os

def getConfig():
  FLASK_ENV = os.getenv('FLASK_ENV')
  if FLASK_ENV == 'production':
    return {
      'sitename': 'Compare Movie Price',
      'timeout': 3,
      'baseURL': 'http://webjetapitest.azurewebsites.net',
      'cinemaList': ['cinemaworld', 'filmworld'],
    }
  else:
    return {
      'sitename': 'Compare Movie Price [Development]',
      'timeout': 3,
      'baseURL': 'http://webjetapitest.azurewebsites.net',
      'cinemaList': ['cinemaworld', 'filmworld'],
    }