#coding: utf-8
from __future__ import with_statement, unicode_literals
from contextlib import closing
import httplib2

# urllib2 doesn't support timeouts for python 2.5


def request(method, url, data=None, headers={}, timeout=None):
    host, _, port = url.split('/')[2].partition(':')
    if not port:
        port = None

    timeout_set = False
    try:
        connection = httplib2.HTTPConnectionWithTimeout(host, port=port, timeout=timeout)
        timeout_set = True
    except TypeError:
        connection = httplib2.HTTPConnectionWithTimeout(host, port=port)

    with closing(connection):
        if not timeout_set:
            connection.connect()
            connection.sock.settimeout(timeout)
            timeout_set = True

        connection.request(method, url, data, headers)
        response = connection.getresponse()
        return (response.status, response.read())
