from twython import TwythonStreamer
import twython

from parsers import parse_tweet
import credentials 

def _print(s):
  print(s)

class StreamHandler(TwythonStreamer):
  """
  A wrapper around Twython's StreamHandler
  """
  def __init__(self, **kw):
    
    TwythonStreamer.__init__(
      self,
      kw.get('api_key', credentials.TWT_API_KEY), 
      kw.get('api_secret', credentials.TWT_API_SECRET),
      kw.get('access_token', credentials.TWT_ACCESS_TOKEN),
      kw.get('access_secret', credentials.TWT_ACCESS_SECRET),
      )
    self.parse = kw.get('parse', parse_tweet)
    self.store = kw.get('store', _print)

  def on_success(self, data):
    print data

  def on_error(self, status_code, data):
    print status_code

class Stream:
  """
  Our public class which simplifies Twython's streaming methods,
  allowing for a `parse` and `store` function to be passed in.
  """
  def __init__(self, **kw):
    self.stream = StreamHandler(
      api_key = kw.get('api_key', credentials.TWT_API_KEY), 
      api_secret = kw.get('api_secret', credentials.TWT_API_SECRET),
      access_token = kw.get('access_token', credentials.TWT_ACCESS_TOKEN),
      access_secret = kw.get('access_secret', credentials.TWT_ACCESS_SECRET),
      parse = kw.get('parse'),
      store = kw.get('store')
    ) 
    self.terms = kw.get('terms')
    self.filter_level = kw.get('filter_level', None)

  def statuses(self, **kw):
    self.stream.statuses.filter(**kw)


if __name__ == '__main__':
  
  s = Stream(parse=parse_tweet, store=_print)
  s.statuses(terms=["hello"])
  


  
