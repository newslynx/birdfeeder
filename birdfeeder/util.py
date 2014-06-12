from functools import wraps
import time 
import twython
import logging
from parsers import parse_tweet
from defaults import default_kws
from connection import connect 

logging.basicConfig()
logger = logging.getLogger("birdfeeder")

def validate_kw(kw, requires):
  """
  Validate kw.
  """
  # check required kwargs
  for r in requires:
    if r not in kw:
      raise Exception(
        "Missing required kwarg: %s" % r
        )

  # insert defaults 
  for k,v in default_kws.items():
    if k not in kw:
      kw[k] = v

  return kw

def opt_connect(**kw):
  """
  Connect to api if we havent passed a `conn` 
  argument in.
  """
  if 'conn' in kw:
    return conn 
  else:
    return connect(**kw)

def get_max_id(tweets):
  """
  Get the max id for a response
  """
  
  ids = [t['id'] for t in tweets if t and 'id' in t]
  
  if len(ids) == 0:
    return None 
  
  else:
    max_id = list(sorted(ids))[0]
    return max_id

def catch_err(func, api, **kw):
  """
  Catch Twitter API Errors, backoff, and timeout.
  """
  
  # get timing kwargs
  wait = kw.get('wait')
  backoff = kw.get('backoff')
  timeout = kw.get('timeout')

  # try until we timeout
  while True:
    try:
      tweets = func(api, **kw)
      break
    
    # backoff from errors
    except twython.exceptions.TwythonError as e:
      t0 = time.time()
      time.sleep(wait)
      wait *= backoff

      # timeout
      now = time.time()
      if now - t0 > timeout:
        logger.warn("Timing out beacause of {0}".format(e))
        tweets = []
        break

  return tweets

def paginate(func, api, **kw):
  """
  Paginate through the api, catching errors 
  and stopping if we finish or reach 
  `max_requests`
  """
  
  # set control variables
  p = 1
  
  # if we passed in a `max_id`, 
  # decrement it by 1
  if kw['max_id']:
    kw['max_id'] = kw['max_id'] - 1

  # hit the api until we should stop
  while True:

    # run the function first
    tweets = catch_err(func, api, **kw)

    # get the max id
    max_id = get_max_id(tweets)
    
    # if we got a max_id, proceed
    if max_id:
      
      # update max_id kwarg
      kw['max_id'] = max_id - 1

      # iterate through tweets
      for t in tweets:
        yield t

    # if we got no max_id break
    else:
      break

    # if we've reached the max number of pages, break 
    max_requests = kw.get('max_requests')
    if max_requests and p > max_requests:
      break
    # increment page
    p += 1

    # throttle requests
    time.sleep(kw.get('throttle')) 
