from twython import Twython 

def connect(**kw):
  """
  Given environmental variables / kw, connect to twitter's api
  """
  
  # load credentials
  app_key = kw.get('app_key', creds.TWT_API_KEY)
  app_secret = kw.get('app_secret', creds.TWT_API_SECRET)
  oauth_token = kw.get('oauth_token', creds.TWT_ACCESS_TOKEN)
  oauth_secret = kw.get('oauth_secret', creds.TWT_ACCESS_SECRET)
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
