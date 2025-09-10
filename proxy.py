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

# Need some sort of main function to define progression:
    # need to create some sort of cache object 
    # then need to listen
    # loop to handle connections
        ## Accept the connection
        ## Create thread and assign it the acception fd as it's argument -> send it to a thread handler
    # close the listen

#Need a thread handler
    #think it takes the argument passed in and gets the fd
    #sends it to the http transaction
    #closes the fd
    
#Http transaction
    #takes a fd as an input 
    #read client request
    #parse the request
    #check in cache
        #check for URL in cache
        #if miss
            #build request
            #send request/open connection to server
            #read server response
            #send to client 
            #store in cache
        #if hit
            #writes cached object directly to client
# fmseflksemflske