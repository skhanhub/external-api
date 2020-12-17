import requests
import concurrent.futures
from datetime import datetime
from services.processMovies import ProcessMovies

class ProcessMovieDetails(ProcessMovies):
  def __init__(self, accessToken = '', baseURL = '', cinemas = [], timeout = 2000):
    self.accessToken = accessToken  
    self.baseURL = baseURL  
    self.cinemas = cinemas  
    self.timeout = timeout  
    self.__cache = {}
    self.lastUpdate = None
   

  def getMovie(self, session, cinema, id):
    headers = {'x-access-token': self.accessToken}
    
    data = {}
    data['cinema'] = cinema
    data['id'] = id

    try:
      response = session.get("{0}/api/{1}/movie/{2}".format(self.baseURL, cinema, id), timeout=self.timeout, headers=headers)
      data['statusCode'] = response.status_code
      data['Movie'] = {'Price': response.json()['Price']}

    except Exception as e:
      data['statusCode'] = 500

    return data

  def generateMovieDetails(self, movie):

    result = {}
    code = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
      futures = []
      with requests.Session() as session:

        for cinema, id in movie.items():
          futures.append(executor.submit(self.getMovie, session=session, cinema=cinema, id=id))

        for future in concurrent.futures.as_completed(futures):
          data = future.result()
          cinema = data['cinema']
          id = data['id']

          if data['statusCode'] == 200:
            self.lastUpdate = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            if cinema in self.__cache:
              self.__cache[cinema][id] = data['Movie']
            else:
              self.__cache[cinema] = {}
              self.__cache[cinema][id] = data['Movie']
            
            result[cinema] = data['Movie']

          elif data['cinema'] in self.__cache and id in self.__cache[cinema]:
            result[cinema] = self.__cache[cinema][id]
            code = 1 
          else:
            code = 1

        if not result:
          code = 2

        return {'cinemas': result, 'code': code, 'lastUpdate': self.lastUpdate}
