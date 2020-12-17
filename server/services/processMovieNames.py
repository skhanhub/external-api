from requests import Session
import concurrent.futures
from datetime import datetime
from services.processMovies import ProcessMovies

class ProcessMovieNames(ProcessMovies):
  def __init__(self, accessToken = '', baseURL = '', cinemas = [], timeout = 2000):
    self.accessToken = accessToken  
    self.baseURL = baseURL  
    self.cinemas = cinemas  
    self.timeout = timeout  
    self.__cache = {}
    self.lastUpdate = None
   

  def getMovies(self, session, cinema):
    headers = {'x-access-token': self.accessToken}
    
    data = {}
    data['cinema'] = cinema

    try:
      response = session.get("{0}/api/{1}/movies".format(self.baseURL, cinema), timeout=self.timeout, headers=headers)
      data['statusCode'] = response.status_code
      data['Movies'] = response.json()['Movies']
        
    except Exception as e:
      data['statusCode'] = 500

    return data

  def generateMovieList (self):
    movies = {}
    code = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
      futures = []
      with Session() as session:

        for cinema in self.cinemas:
          futures.append(executor.submit(self.getMovies, session=session, cinema=cinema))

        for future in concurrent.futures.as_completed(futures):
          data = future.result()
          source = {}
          if data['statusCode'] == 200:
            self.lastUpdate = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            self.__cache[data['cinema']] = data['Movies']
            source = data['Movies']

          elif data['cinema'] in self.__cache:
            code = 1
            source = self.__cache[data['cinema']]
            
          if source:
            for movie in source:
                if movie['Title'] in movies:
                  movies[movie['Title']][data['cinema']] = movie['ID']
                else:
                  movies[movie['Title']] = {}
                  movies[movie['Title']][data['cinema']] = movie['ID']
            

        if not movies:
          code = 2
        
        return {'movies': movies, 'code': code, 'lastUpdate': self.lastUpdate}
