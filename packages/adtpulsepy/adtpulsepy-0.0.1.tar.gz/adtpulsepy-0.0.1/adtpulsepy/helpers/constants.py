"""ADT Pulse constants."""
import os

MAJOR_VERSION = 0
MINOR_VERSION = 0
PATCH_VERSION = '1'

__version__ = '{}.{}.{}'.format(MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)

REQUIRED_PYTHON_VER = (3, 4, 2)

PROJECT_NAME = 'adtpulsepy'
PROJECT_PACKAGE_NAME = 'adtpulsepy'
PROJECT_LICENSE = 'Apache 2.0'
PROJECT_AUTHOR = 'Ty Amell'
PROJECT_COPYRIGHT = ' 2018, {}'.format(PROJECT_AUTHOR)
PROJECT_URL = 'https://github.com/tyamell/adtpulsepy'

PROJECT_DESCRIPTION = ('An ADT Pulse client using their undocumented API.')
PROJECT_LONG_DESCRIPTION = ('adtpulsepy is an open-source '
                            'unofficial API for the ADT Pulse alarm '
                            'system')
if os.path.exists('README.rst'):
    PROJECT_LONG_DESCRIPTION = open('README.md').read()

PROJECT_CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.4',
    'Topic :: Home Automation'
]

PROJECT_GITHUB_USERNAME = 'tyamell'
PROJECT_GITHUB_REPOSITORY = 'adtpulsepy'

PYPI_URL = 'https://pypi.python.org/pypi/{}'.format(PROJECT_PACKAGE_NAME)

CACHE_PATH = './adtpulse.pickle'



# URLS
BASE_URL = 'https://api.adtpulse.com/ng/rest/adt/'

LOGIN_URL = BASE_URL + 'access/login'
LOGOUT_URL = BASE_URL + 'ui/client/site/signOut'
UPDATES_URL = BASE_URL + 'ui/updates'


MODE_AWAY = 'away'
MODE_STAY = "stay"
