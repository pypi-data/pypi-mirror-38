# brevis-python-client
Python Client for the [Brevis](https://github.com/admiralobvious/brevis) URL shortener API

## How-to use

```
>>> import brevis
>>> client = brevis.BrevisClient('https://brevis-server')
>>> short = client.shorten('https://google.com')
>>> print(short)
{'short_url': 'https://brevis-test.klik.co/Hz9YqVphB'}
>>> long = client.unshorten(short['short_url'])
>>> print(long)
{'url': 'https://google.com'}
```
