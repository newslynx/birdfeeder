from twython import TwythonStreamer
import twython

from parsers import parse_tweet
import credentials

def _print(d):
  print(d)

def _pass(s, d):
  pass

class Stream(TwythonStreamer):
  """
  A wrapper around Twython's StreamHandler
  """
  def __init__(self, **kw):
    
    TwythonStreamer.__init__(
      self,
      kw.get('app_key', credentials.TWT_API_KEY),
      kw.get('app_secret', credentials.TWT_API_SECRET),
      kw.get('oauth_token', credentials.TWT_ACCESS_TOKEN),
      kw.get('oauth_token secret', credentials.TWT_ACCESS_SECRET)
      )
    self.parse = kw.get('parse', parse_tweet)
    self.store = kw.get('store', _print)
    self.error = kw.get('error', _pass)

  def on_success(self, data):
    self.store(self.parse(data))

  def on_error(self, status_code, data):
    self.error(status_code, data)
  
