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

def cachefile(url: bytes) -> str:
    """Return a specific filename to use for caching the given URL.

    Please use this to generate cache filenames, passing it the full URL as
    given in the client request.  (This will help me write tests for grading.)
    """
    return "cache/" + hashlib.sha256(url).hexdigest()


def pe(*args, **kwargs):
    """Print to standard error.

    Nothing earth-shattering here, just saves typing.  Use exactly the same as
    you would the print() function.
    """
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)


### Your code here! ###

def make_cache():
    try:
        os.makedirs("cache", exist_ok=True)
    except Exception as e:
        pe("Error making cache", e)

# Need some sort of main function to define progression:
    # need to create some sort of cache object 
        # cache_line object 
        # or could just be a dictionary, pohly said wasn't too much constraint. 
        # just make a hashmap with url and cached file
    # then need to listen
    # loop to handle connections
        ## Accept the connection
        ## Create thread and assign it the accepted fd as its argument -> send it to a thread handler
    # close the listen


# Need a thread handler
    # think it takes the argument passed in and gets the fd
    # sends it to the http transaction
    # closes the fd

# Http transaction
    # takes a fd as an input 
    # read client request
    # parse the request
    # check in cache
        # check for URL in cache
        # if miss
            # build request
            # send request/open connection to server
            # read server response
            # send to client 
            # store in cache
        # if hit
            # writes cached object directly to client
def http_transaction(conn: socket.socket, addr):
    try:
        # read the full request (headers end with \r\n\r\n)
        data = b""
        while b"\r\n\r\n" not in data:
            chunk = conn.recv(BUFSIZ)
            if not chunk:
                break
            data += chunk
        if not data:
            return

        # parse first line
        first_line, remains = data.split(b"\r\n", 1)
        method, link, version = first_line.split(b" ", 2)

        # sanity check – must be a GET (fix: compare bytes to bytes)
        if method != b"GET":
            return

        # check cache
        try:
            with open(cachefile(link), "rb") as cache_file:
                while True:
                    chunk = cache_file.read(BUFSIZ)
                    if not chunk:
                        break
                    conn.sendall(chunk)
            return
        except FileNotFoundError:
            # miss – forward to origin
            request, host, port = create_request(link)
            server_conn = send_request(request, host.decode(), port)
            read_response(server_conn, conn, link)
    finally:
        try:
            conn.close()
        except:
            pass


def create_request(link: bytes):
    # Accept absolute-form (http://host:port/path) or fallback
    if link.startswith(b"http://"):
        _, remainder = link.split(b"http://", 1)
    else:
        remainder = b"localhost:80" + link

    # static headers
    connection_h = b"Connection: close\r\n"
    proxy_h = b"Proxy-Connection: close\r\n"
    user_h = b"User-Agent: " + USER_AGENT + b"\r\n"

    # find host port path
    if b":" in remainder:
        colon_pos = remainder.find(b":")
        slash_pos = remainder.find(b"/", colon_pos)
        host = remainder[:colon_pos]
        if slash_pos == -1:
            port_h = int(remainder[colon_pos + 1:] or b"80")
            path = b"/"
        else:
            port_h = int(remainder[colon_pos + 1:slash_pos] or b"80")
            path = remainder[slash_pos:] or b"/"
    else:
        slash_pos = remainder.find(b"/")
        host = remainder[:slash_pos] if slash_pos != -1 else remainder
        port_h = 80
        path = remainder[slash_pos:] if slash_pos != -1 else b"/"

    # get hdr
    get_h = b"GET " + path + b" HTTP/1.0\r\n"

    # host hdr
    host_h = b"Host: " + host + b"\r\n"

    return get_h + host_h + user_h + connection_h + proxy_h + b"\r\n", host, port_h


def send_request(request: bytes, host: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(request)
    return sock


def read_response(server_conn: socket.socket, client_conn: socket.socket, url: bytes):
    total_resp = b""

    # read bytes
    while True:
        buf = server_conn.recv(BUFSIZ)
        if not buf:
            break
        client_conn.sendall(buf)
        total_resp += buf

    try:
        server_conn.close()
    except:
        pass

    # write to file
    with open(cachefile(url), "wb") as f:
        f.write(total_resp)


def main(port: int):
    make_cache()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set option BEFORE bind; SO_REUSEADDR is portable
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", port))
    sock.listen(50)  # backlog val

    while True:
        conn, addr = sock.accept()
        # spawn a thread per connection
        t = threading.Thread(target=http_transaction, args=(conn, addr), daemon=True)
        t.start()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: ./proxy.py <port>", file=sys.stderr)
        sys.exit(1)
    main(int(sys.argv[1]))
