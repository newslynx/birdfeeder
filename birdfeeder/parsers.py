#!/usr/bin/env python
# -*- coding: utf-8 -*-

from siegfried import is_short_url, unshorten_url, prepare_url
from datetime import datetime
import pytz

TWT_DATE_FORMAT = '%a %b %d %H:%M:%S +0000 %Y'

def utc_now():
  dt = datetime.utcnow()
  dt = dt.replace(tzinfo = pytz.utc)
  return dt

def get_url_candidates(e):
  """
  Get all urls in the tweet
  """
  candidates = set()
  for url in e.get('urls', []):
    if url:
      candidates.add(url['expanded_url'])
  return list(candidates)

def parse_url(url):
  """
  unshorten and/or normalize url.
  """
  if is_short_url(url):
    long_url = unshorten_url(url)
    if long_url:
      return prepare_url(long_url)
    else:
      return url
  else:
    return prepare_url(url)

def get_urls(e):
  urls = set()
  candidates = get_url_candidates(e)
  if len(candidates)==0:
    return []
  for url in candidates:
    if url:
      urls.add(parse_url(url))
  return list(urls)

def get_datetime(tweet):
  dt = datetime.strptime(tweet['created_at'], TWT_DATE_FORMAT)
  dt = dt.replace(tzinfo = pytz.utc)
  return dt

def get_hashtags(e):
  hashtags = set()
  candidates = e.get('hashtags', [])
  if len(candidates) == 0:
    return []
  for c in candidates:
    hashtags.add(c.get('text'))
  return list(hashtags)

def get_user_mentions(e):
  mentions = set()
  candidates = e.get('user_mentions', [])
  if len(candidates) == 0:
    return []
  for c in candidates:
    mentions.add(c['screen_name'])
  return list(mentions)

def get_img_urls(e):
  img_urls = set()
  media = e.get('media', [])
  for m in media:
    if m:
      img_urls.add(m.get('expanded_url'))
  return list(img_urls)

def parse_tweet(tweet):
  
  # get nested dicts
  e = tweet.get('entities', {})
  user = tweet.get('user', {})
  
  # extract
  return {
    'twitter_id': tweet.get('id_str', None),
    'text': tweet.get('text', '').encode('utf-8'),
    'datetime': get_datetime(tweet),
    'in_reply_to_screen_name': tweet.get('in_reply_to_screen_name'),
    'in_reply_to_status_id': tweet.get('in_reply_to_status_id_str'),
    'urls': get_urls(e),
    'hashtags': get_hashtags(e),
    'user_mentions': get_user_mentions(e),
    'img_urls': get_img_urls(e),
    'screen_name': user.get('screen_name', None),
    'verified': 1 if user.get('verified', False) else 0, # convert bool
    'user_location': user.get('location', None)
  }

def parse_user_stats(user, screen_name):
  return {
    'datetime' : utc_now(),
    'screen_name' : screen_name,
    'favorites' : user.get('favourites_count', None),
    'followers' : user.get('followers_count', None),
    'friends' : user.get('friends_count', None),
    'listed' : user.get('listed_count', None),
    'statuses' : user.get('statuses_count', None)
  }


