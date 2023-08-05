"""
adtpulsepy - An ADT Pulse alarm Python library.

"""

import logging
import requests
from adtpulsepy.devices.alarm import ADTPulseAlarm
import adtpulsepy.helpers.constants as CONST
import adtpulsepy.helpers.util as UTIL
from adtpulsepy.exceptions import (ADTPulseAuthException,
                                   ADTPulseException)

_LOGGER = logging.getLogger(__name__)

class ADTPulse():
    """Main ADT Pulse class."""

    def __init__(self, username=None, password=None,
                 auto_login=False):
        """Init ADT object."""

        if username is None or password is None:
            raise ValueError("""Username and password must
            be provided for auto login.""")

        self._session = None
        self._token = None
        self._username = username
        self._password = password
        self._alarms = []

        self._default_alarm_mode = CONST.MODE_AWAY

        self._devices = None

        self._first_update = True

        # Create a requests session to persist the cookies
        self._session = requests.Session()

        if auto_login and username is not None and password is not None:
            self.login()
            self.update()

    def _get_headers(self):
        """Returns the HTTP Headers needed for all calls."""
        return {
            'X-password': self._password,
            'X-appKey': 'XahAvedeZeJmeLeTeDEburyubAqUnu6uXe',
            'User-Agent': 'Pulse/2 CFNetwork/974.2.1 Darwin/18.0.0',
            'X-login': self._username,
            'X-format': 'json',
            'X-expires': '2592000000',
            'X-locale': 'en_us',
            'X-version': '4.4',
            'X-clientType': 'CUSTOM_IPHONE',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def login(self):
        """Explicit Abode login."""
        self._token = None

        response = self._session.post(CONST.LOGIN_URL,
                                      headers=self._get_headers())
        login_payload = response.json()

        if response.status_code != 200:
            raise ADTPulseAuthException((response.status_code,
                                         login_payload['detail']
                                         .replace('<br/>', '\n')))

        self._cookies = response.cookies
        self._token = login_payload['detail']

        _LOGGER.info("Login successful")

        return True

    @property
    def alarm(self):
        """Gets all the ADT Pulse Alarm device."""
        return self._get_alarm()

    def _get_alarm(self):
        """Indirect accessor to return 'alarm' property."""
        self.update()
        return self._alarms[0]

    @property
    def sensors(self):
        """Gets all the ADT Pulse sensors."""
        return self._get_sensors()

    def _get_sensors(self):
        """Indirect accessor to return 'sensors' property."""
        self.update()
        return self._alarms[0].sensors


    def update(self):
        """Call the updates API for ADT Pulse, getting
        updated json with the status on the alarm and devices"""
        if self._token is None:
            self.login()
        resp = self._session.get(CONST.UPDATES_URL, headers=self._get_headers())
        data = UTIL.load_dirty_json(resp.text)
        for upd in data["update"]:
            self._alarms.append(ADTPulseAlarm(upd["data"]["client"]))

