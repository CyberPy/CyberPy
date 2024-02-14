from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library
standard_library.install_aliases()
from builtins import str

try:
	from oauth2client import client, crypt
except ImportError:
	print('''
Warning: Google API lib not found.
Do not use cyberpy.GoogleUser''')

from http.cookies import SimpleCookie as Cookie
from email.mime.multipart import MIMEMultipart
from os import listdir, mkdir, makedirs, rmdir
from wsgiref.handlers import format_date_time
from wsgiref.simple_server import make_server
from base64 import b64encode, b64decode
from urllib.parse import quote, unquote
from os import rename, remove, urandom
from email.mime.text import MIMEText
from collections import OrderedDict
from cgi import escape, parse_qs
from sys import path as SYSPath
from os import path as OSPath
from datetime import datetime
from types import MethodType
from platform import system
from random import randint
from gzip import GzipFile
from smtplib import SMTP
from sys import exc_info
from uuid import uuid4
from io import BytesIO
from gc import collect
from time import time
import requests
import hashlib
import MySQLdb
import inspect
import _thread
import json

def text(val):
    if isinstance(val, bytes):
        val = val.decode('utf-8')
    elif isinstance(val, str):
        pass
    else:
        err = ' '.join((
            "Expected 'bytes' or 'str', got",
            str(type(val)), 'instead'))
        raise TypeError(err)
    return val

def untext(val):
    if isinstance(val, bytes):
        pass
    elif isinstance(val, str):
        val = val.encode('utf-8')
    else:
        err = ' '.join((
            "Expected 'bytes' or 'str', got",
            str(type(val)), 'instead'))
        raise TypeError(err)
    return val

def encode_uri(uri):
    return quote(text(uri).replace(
        '/', '-d-'),
        safe="~()*!.\'")

def decode_uri(uri):
    return unquote(text(uri
    )).replace('-d-', '/')

def escape_sql(sql, encode=True):
    if encode:
        sql = encode_uri(sql)
    return sql.replace("'", "\\'"
    ).replace("\Z", "\\Z")
