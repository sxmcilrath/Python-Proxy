#!/usr/bin/env python3

# Add your own imports as needed
import sys
import hashlib


# Feel free to substitute this as the User-Agent header in your outgoing requests
USER_AGENT = b'Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'

# A buffer size.  Use when buffers have sizes.  Recommended over reading entire
# files or responses into a single bytes object, which may not be particularly
# good when I'm trying to listen to di.fm using the proxy.
BUFSIZ = 4096


# Some helper functions

def cachefile(url):
    """Return a specific filename to use for caching the given URL.

    Please use this to generate cache filenames, passing it the full URL as
    given in the client request.  (This will help me write tests for grading.)
    """
    return 'cache/' + hashlib.sha256(url).hexdigest()

def pe(*args, **kwargs):
    """Print to standard error.

    Nothing earth-shattering here, just saves typing.  Use exactly the same as
    you would the print() function.
    """
    kwargs['file'] = sys.stderr
    print(*args, **kwargs)


### Your code here! ###
