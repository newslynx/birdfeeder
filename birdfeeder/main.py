from twython import Twython 

from parsers import parse_user_stats
import credentials
from util import *

"""
Defaults for all tweet functions.
"""

default_kws = {
  'paginate' : False,
  'max_id': None,
  'throttle' : 15,
  'count' : 200,
  'max_requests' : None,
  'wait': 1,
  'backoff': 2,
  'timeout': 30  # timeout for a bit over the rate limit.
}

def connect(**kw):
  """
  Given environmental variables / kw, connect to twitter's api
  """
  
  # load credentials
  app_key = kw.get('app_key', credentials.TWT_API_KEY)
  app_secret = kw.get('app_secret', credentials.TWT_API_SECRET)
  oauth_token = kw.get('oauth_token', credentials.TWT_ACCESS_TOKEN)
  oauth_secret = kw.get('oauth_secret', credentials.TWT_ACCESS_SECRET)
  access_token = kw.get('access_token', None)

  conn = Twython(
    app_key = app_key,
    app_secret = app_secret,
    oauth_token = oauth_token,
    oauth_token_secret = oauth_secret,
    access_token = access_token
    )

  # authenticate
  return conn


def twt(requires=[], default={}):
  """
  A decorator for a tweet function.
  Includes kwarg validation, optional
  api connection, inclusion of default 
  kwargs, error handling, pagination,
  and tweet parsing.
  """
  def twt_func(func):  
    @wraps(func)
    def f(*args, **kw):
      
      # check kw's
      kw = validate_kw(kw, requires)

      # optionally connect to the api
      api = opt_connect(**kw)

      # add defautls to kw's
      kw = dict(kw.items() + default.items())

      # if were not paginating simply
      # run the function
      if not kw['paginate']:
        
        tweets = catch_err(func, api, **kw)
        for t in tweets:
          yield parse_tweet(t)

      # otherwise proceed with pagination
      else:
        for t in paginate(func, api, **kw):
          yield parse_tweet(t)
  
    return f
  return twt_func


@twt(requires=['owner_screen_name', 'slug'])
def list_timeline(api, **kw):
  """
  Get all tweets from a list
  """  
  # get tweets
  return api.get_list_statuses(**kw)


@twt(requires=['q'], default = {'result_type' : 'recent'})
def search(api, **kw):
  """
  Search twitter
  """  
  # connect
  tweets = api.search(**kw)
  return tweets['statuses']


@twt(requires=['screen_name'])
def user_timeline(api, **kw):
  """
  Get tweets from a users timeline
  """  
  return api.get_user_timeline(**kw)


def user_stats(**kw):
  """
  Get stats about a user. 
  Since we're using a different parser
  and not paginating we wont use
  the decorator 
  """
  def _get_user(api, **kw):
    return api.show_user(**kw)

  # connect
  kw = validate_kw(kw, ['screen_name'])
  api = opt_connect(**kw)
  screen_name = kw.get('screen_name')
  user = catch_err(_get_user, api, **kw)
  return parse_user_stats(user, screen_name)

if __name__ == '__main__':
  for t in search(q="towcenter", paginate=True):
    print t
