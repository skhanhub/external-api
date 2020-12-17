class ProcessMovies:
  def __init__(self, accessToken = '', baseURL = '', cinemas = [], timeout = 500):
    self.accessToken = accessToken  
    self.baseURL = baseURL  
    self.cinemas = cinemas  
    self.timeout = timeout  

  def setAccessToken(self, accessToken):
    self.accessToken = accessToken
    return accessToken

  def setBaseURL(self, baseURL):
    self.baseURL = baseURL
    return baseURL

  def setCinemas(self, cinemas):
    self.cinemas = cinemas
    return cinemas

  def setTimeout(self, timeout):
    self.timeout = timeout
    return timeout