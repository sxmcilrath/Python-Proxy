#!/usr/bin/env python3

# Add your own imports as needed
import sys
import hashlib
import socket
import threading
import os


# Feel free to substitute this as the User-Agent header in your outgoing requests
USER_AGENT = b'Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'

# A buffer size.  Use when buffers have sizes.  Recommended over reading entire
# files or responses into a single bytes object, which may not be particularly
# good when I'm trying to listen to di.fm using the proxy.
BUFSIZ = 4096

# GLOBAL VARS
cache = {}


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
        #cache_line object 
        #or could just be a dictionary, pohly said wasn't too much constraint. 
        #just make a hashmap with url and cached file
    # then need to listen
    # loop to handle connections
        ## Accept the connection
        ## Create thread and assign it the acception fd as it's argument -> send it to a thread handler
    # close the listen
def main(port):

    sock = socket.socket()
    sock.bind(('', port))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.listen() #backlog val default

    while True:
        conn, addr = sock.accept()
        t = threading.Thread(target=http_transaction, args=(conn, addr))
        t.start()

# if __name__ == "__main__":
#     main()

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
def http_transaction(conn: socket.socket, addr):
    #parse requests
    data = conn.recv(BUFSIZ)
    #err check
    if not data:
        #NEED TO INSERT PERROR equiv
        conn.close()
        return
    
    first_line, remains = data.split(b"\r\n",1)
    method, link, version = first_line.split(b" ", 2)
    assert method == "GET" #sanity check

    #check cache
    try:
        cache_file = open(f"cache/{cachefile(link)}", "r")
        cache_msg = cache_file.read(BUFSIZ)
        conn.sendall(cache_msg)
        return
    except Exception as ex:
        create_request(link)
    #cleanup
    conn.close()

def create_request(link: bytes):

    trash, remainder = link.split(b"http://", 1)

    #get port and host
    port = 80
    host = b"Host: "
    if b":" in remainder:
        port =  remainder[remainder.find(b":")+1 : remainder.find(b"/")]
        host += remainder.split(b":", 1)[0] + b"\r\n"
    else:
        host = remainder.split(b"/", 1)[0] + b"\r\n"


    #get host
    
    
    return None