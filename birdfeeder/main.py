from functools import wraps
from parsers import parse_user_stats, parse_tweet
import credentials as creds
from util import (
  paginate, catch_err, validate_kw, 
  opt_connect, concurrent_yield
)


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
      else:
        tweets = paginate(func, api, **kw)

      # optionally run concurrent
      if kw['concurrent']:
        return concurrent_yield(parse_tweet, tweets, **kw)

      else:
        return (parse_tweet(t) for t in tweets)
  
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
  for t in user_timeline(screen_name="brianabelson", paginate=True, concurrent=True):
    print t
