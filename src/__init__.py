# coding=utf-8


# CyberPy
# (c) 2023
# https://github.com/CyberPy
# License: MIT

from __future__ import absolute_import
from __future__ import unicode_literals
from .module import Module
Module.main_access(__name__)

from .dependencies import *
from .pygod import *
from .controlflow import *

# default MySQL settings
# point to localhost,
# reset these in MAIN.settings

HOSTNAME = '' # 127.0.0.1
PORTNUMBER = 3306
USERNAME = '' # root
PASSWORD = '' # root
SEPARATOR = '$' # None # unreferenced?
LOG_ENABLED = False

# default GAPI settings
# (dummy text), set these
# in MAIN.settings

CLIENTID = 'CLIENTID.apps.googleusercontent.com'
SCOPES = 'profile email'

# set login details
# (for Email class)
# in MAIN.settings

EMAIL = '' # 'info@example.com'
EMAIL_PW = '' # ''

# set DOMAIN, logo,
# & NAME in
# main script for
# Email class, and db_name
# in MAIN.settings

DOMAIN = '' # http://localhost:8000/
LOCAL_DOM = DOMAIN
LOCALHOST = False # True
NAME = '' # localdb
ALTNAME = None
KNOWN_BRAND = False
LOGO_URL = None
DEF_LANG = None
DEF_COUNTRY = None
DEF_STATE = None
LONG = None
LAT = None
PLACENAME = None
SIGNIN = 'onSignIn'
ADMIN_PAGES = []

# for metaDATA. set
# these dynamically
# in MAIN.settings

CACHE = True
EXPIRES = '604800' # 1 week
STATIC_EXPIRES = '2592000' # 30 days
USER_EXPIRES = 3600 # 1 hour
SAME_SITE = 'lax'
TITLE = None # (optional)
DESCR = None
ROBOTS = None # (optional)
OGTYPE = None
LANG = Switch()
DATA = Switch()
USER = None # (optional)

# sets in wsgi class

MODES = Switch()
LIVE_URL = None

# set these in MAIN / MAIN.settings
WEBS = Switch()
META_CLASS = None
BODY_CLASS = None
NAV_CLASS = None
NOT_FOUND = None
USER_CLASS = None
MAP_CLASS = None
DEV_MODE = False
ACTIONS = []
CENSOR = None

from .cyberstring import *
from .filemanager import *
from .cyberfile import *
from .organizer import *
from .errors import *
from .path import *
from .model import *
from .api import *
from .cybermail import *
from .password import *
from .cybertime import *
from .cyberuser import *
from .meta import *
from .hypertext import *
from .cyberxml import *
from .schema import *
from .cyberhtml import *
from .userinterface import *
from .pythonmyadmin import *
from .webinterface import *
from .cyberpack import cyberpack, unpack