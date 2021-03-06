# coding: utf-8
from __future__ import unicode_literals
"""
Yandex.Maps API wrapper
"""

import six
import xml.dom.minidom
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
from yandex_maps import http

STATIC_MAPS_URL = 'http://static-maps.yandex.ru/1.x/?'
HOSTED_MAPS_URL = 'http://maps.yandex.ru/?'
GEOCODE_URL = 'http://geocode-maps.yandex.ru/1.x/?'

def _format_point(longitude, latitude):
    return '%0.7f,%0.7f' % (float(longitude), float(latitude),)

def get_map_url(api_key, longitude, latitude, zoom, width, height):
    ''' returns URL of static yandex map '''
    point = _format_point(longitude, latitude)
    params = [
       'll=%s' % point,
       'size=%d,%d' % (width, height,),
       'z=%d' % zoom,
       'l=map',
       'pt=%s' % point,
       'key=%s' % api_key
    ]
    return STATIC_MAPS_URL + '&'.join(params)


def get_external_map_url(longitude, latitude, zoom=14):
    ''' returns URL of hosted yandex map '''
    point = _format_point(longitude, latitude)
    params = dict(
        ll = point,
        pt = point,
        l = 'map',
    )
    if zoom is not None:
        params['z'] = zoom
    return HOSTED_MAPS_URL + urlencode(params)


def geocode(api_key, address, timeout=2):
    ''' returns (longtitude, latitude,) tuple for given address '''
    try:
        xml = _get_geocode_xml(api_key, address, timeout)
        return _get_coords(xml)
    except IOError:
        return None, None

def _get_geocode_xml(api_key, address, timeout=2):
    url = _get_geocode_url(api_key, address)
    status_code, response = http.request('GET', url, timeout=timeout)
    return response

def _get_geocode_url(api_key, address):
    if isinstance(address, six.text_type):
        address = address.encode('utf8')
    params = urlencode({'geocode': address, 'key': api_key})
    return GEOCODE_URL + params

def _get_coords(response):
    try:
        dom = xml.dom.minidom.parseString(response)
        pos_elem = dom.getElementsByTagName('pos')[0]
        pos_data = pos_elem.childNodes[0].data
        return tuple(pos_data.split())
    except IndexError:
        return None, None
