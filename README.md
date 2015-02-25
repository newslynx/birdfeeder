![travis-img](https://travis-ci.org/newslynx/birdfeeder.svg)
birdfeeder
======
_Feed on tweets_

## Install

```
pip install birdfeeder
```

## Test

Requires `nose`

```
nosetests
```

## Usage

`birdfeeder` simplifies `twython` by taking care of alot the common problems in working with the Twitter API, including:

* pagination
* rate limiting
* url unshortening
* error handling

Thus far, we've implemented 5 methods: `connect`, `search`, `list_timeline`, `user_timeline`, and `user_stats` (a custom method):

### Connect

If you have `TWT_API_KEY`, `TWT_API_SECRET`, `TWT_ACCESS_TOKEN`, and `TWT_ACCESS_SECRET` set as environmental variables, you can use all the methods without explicitly connecting.  However, if you want to explicitly connect beforehand, you can also pass in a connection as `conn` to any method:

```python
import birdfeeder

conn = birdfeeder.connect() 

tweets = birdfeeder.search(q="hello world", count=10, conn=conn)
for t in tweets:
  print t
```

In addition, you can also pass in an authenticated user's token with `access_token`:

```python
import birdfeeder

for t in birdfeeder.search(q="hello world", access_token="authenticed_users_token"):
  print t
```

### Search

```python
import birdfeeder

tweets = birdfeeder.search(q="hello world", count=10)
for t in tweets:
  print t
```

### List Timeline

```python
import birdfeeder

tweets = birdfeeder.list_timeline(owner_screen_name = 'cspan', slug = 'members-of-congress', count=100)
for t in tweets:
  print t 
```

### User Timeline

```python
import birdfeeder 

tweets = birdfeeder.user_timeline(screen_name = 'newslynx')
for t in tweets:
  print t
```

### User Stats 

This returns a dictionary of stats about a user, with the time it ran. It's intended for creating a time series of a user's metadata:

```python
import birdfeeder 

stats = birdfeeder.user_stats(screen_name = "newslynx")
print stats
```

## Pagination

With `birdfeeder`, pagination is simple, just add `paginate=True` to any method, ie:

```python
import birdfeeder

tweets = birdfeeder.user_timeline(screen_name = 'newslynx', count = 5, paginate=True)
for t in tweets:
  print t
```

This will keep track of the `max_id` of each request and iterate through results until everything has been retrieved (or until otherwise specified - more below). For each request, it will wait for a defualt of 15 seconds so as to avoid rate limiting.

## Concurrency
add concurrency to any method via `gevent`:
```python

tweets = birdfeeder.user_timeline(screen_name="brianabelson", concurrent=True)
for t in tweets:
  print t
```

## Custom Options
We've added some custom options for each method, they are as follows:

* `throttle` - the time in seconds to wait between each request (only relevant when `paginate = True`)
* `max_requests` - the maximum number of requests to make (only relevant when `paginate = True`)
* `wait` - the default number of seconds to wait after an error
* `backoff` - the factor to multiply `wait` by after each error 
* `timeout` - the time in seconds at which point we should abandon an error prone request. Here, `birdfeeder` will log a warning, but will otherwise fail silently.

Here are the default arguments for all methods:

```python
default_kws = {
  'paginate' : False,
  'concurrent': False,
  'num_workers': 20,
  'max_id': None,
  'throttle' : 15,
  'count' : 200,
  'max_requests' : None,
  'wait': 1,
  'backoff': 2,
  'timeout': 30
}
```

## Streaming 

Finally, we've included a simple streaming API client (from [here](http://twython.readthedocs.org/en/latest/usage/streaming_api.html)).
With this, you can pass in three functions on initialization: a parsing function, a storage function, and an error function, ie:

```python
from birdfeeder import Stream 

def parse(data):
  return data['text']

def store(data):
  print data 

def error(status_code, data):
  pass

s = Stream(parse=parse, store=store, error=error)
s.statuses.filter(track='twitter')
```

## Acknowledgements 

To write this library, I heavily referenced Jeremy Singer-Vine's excellent [`twick`](https://github.com/jsvine/twick).



