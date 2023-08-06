"""
API Calls.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import logging
import requests
from pymotion.const import URL

LOGGER = logging.getLogger(__name__)


class API(object):
    """A class for API calls."""

    def __init__(self, host, port):
        """Initialize the class."""
        self._host = host
        self._port = port

    def api_call(self, endpoint=''):
        """Get result from API call."""
        url = URL.format(host=self._host, port=self._port, endpoint=endpoint)
        api_response = {}
        try:
            raw = requests.get(url).text
            api_response = raw

        except requests.exceptions.ConnectionError as error:
            LOGGER.error('Error connecting to Motion Webcontrol %s', error)
            api_response = None
        return api_response

    def list_cameraes(self):
        """Return all cameras."""
        LOGGER.debug("Getting cameraes.")
        cameraes = []
        api_response = self.api_call().split('\n')[2:-1]
        for camera in api_response:
            try:
                endpoint = camera + '/config/get?query=text_left'
                raw = self.api_call(endpoint)
                name = raw.split('\n')[0].split(' = ')[1]
                endpoint = camera + '/config/get?query=stream_port'
                raw = self.api_call(endpoint)
                stream_port = raw.split('\n')[0].split(' = ')[1]
                stream = URL.format(host=self._host, port=stream_port,
                                    endpoint='')
                cameraes.append({'id': camera, 'name': name, 'stream': stream})
            except (TypeError, IndexError, KeyError) as error:
                LOGGER.error('Error connecting to Motion Webcontrol %s', error)
        LOGGER.debug(api_response)
        return cameraes
