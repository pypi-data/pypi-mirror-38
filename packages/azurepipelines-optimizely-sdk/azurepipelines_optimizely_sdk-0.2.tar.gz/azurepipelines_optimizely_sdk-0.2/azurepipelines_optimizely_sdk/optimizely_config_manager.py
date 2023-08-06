import requests
from optimizely import optimizely
from optimizely.logger import SimpleLogger

class OptimizelyConfigManager(object):
  optimizelyInstance = None

  def __init__(self, projectId):
    self.projectId = projectId

  def getOptimizelyInstance(self):
    if not self.optimizelyInstance:
      self.setOptimizelyInstance()
    return self.optimizelyInstance

  def setOptimizelyInstance(self, url=None):
    if not url:
      url = 'https://cdn.optimizely.com/json/{0}.json'.format(self.projectId)

    datafile = self.fetchDataFile(url)
    self.optimizelyInstance = optimizely.Optimizely(datafile, None, SimpleLogger())

  def fetchDataFile(self, url):
    datafile = requests.get(url).text
    return datafile