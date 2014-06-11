![travis-img](https://travis-ci.org/newslynx/birdfeeder.svg)
birdfeeder
======
_A newslynx-opinionated wrapper around twython_

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
* authentication

* pagination
* rate limiting
* url unshortening
* error handling

Thus far, we've implemented 4 methods: `search`, `list_timeline`, `user_timeline`, and `user_stats`:

### `birdfeeder.search`
```python
from birdfeeder import search, connect

tweets = search(q)

