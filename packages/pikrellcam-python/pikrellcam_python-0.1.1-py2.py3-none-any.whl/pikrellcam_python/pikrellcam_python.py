"""Define a PiKrellCam device."""

from typing import List, Type, TypeVar, Union  # noqa
from aiohttp import BasicAuth, ClientSession
from aiohttp.client_exceptions import ClientError
import logging


_LOGGER = logging.getLogger(__name__)

ApiType = TypeVar('ApiType', bound='PiKrellCam')


class PiKrellCam:
    """Define an object to interact with a PiKrellCam instance."""

    def __init__(self, websession: ClientSession) -> None:
        """Initialize."""
        self._websession = websession
        self._auth = None
        self._base_url = None
        self.state_data = {}
        self._available = True

    @classmethod
    async def login(
            cls: Type[ApiType], host: str, port: str, user: str, password: str,
            websession: ClientSession) -> ApiType:
        """Create an API object from a email address and password."""
        klass = cls(websession)
        klass._base_url = 'http://{0}:{1}/'.format(host, port)
        klass._auth = BasicAuth(login=user, password=password)
        await klass._request('get', '')
        return klass

    async def _request(
            self,
            method: str,
            endpoint: str) -> str:

        """Make a request."""
        url = '{0}{1}'.format(self._base_url, endpoint)

        try:
            async with self._websession.request(method,
                                                url,
                                                auth=self._auth) as resp:
                self._available = True
                return await resp.text()

        except ClientError as error:
            _LOGGER.error('Failed to communicate with PiKrellCam: %s', error)
            self._available = False
            return

    async def is_motion_enabled(self) -> str:
        return self.state_data.get('motion_enable')

    async def is_recording(self) -> str:
        return self.state_data.get('video_record_state')

    async def update(self):
        """Fetch the latest state data from PiKrellCam."""
        resp = await self._request('get', 'state')
        if resp:
            for line in resp.splitlines():
                key, val = line.strip().split(None, 1)
                if val == 'on' or val == 'off':
                    val = (val == 'on')
                    self.state_data[key] = val
                else:
                    self.state_data[key] = val

    @property
    def available(self):
        """Return True if is available."""
        return self._available

    @property
    def base_url(self):
        """Return the base url for endpoints."""
        return self._base_url

    @property
    def mjpeg_url(self):
        """Return mjpeg url."""
        return "{}/mjpeg_stream.php".format(self.base_url)

    @property
    def image_url(self):
        """Return snapshot image url."""
        return "{}/mjpeg_read.php".format(self.base_url)

    def change_setting(self, key, val):
        """Change a setting.

        Return a coroutine.
        """
        if isinstance(val, bool):
            payload = 'on' if val else 'off'
        else:
            payload = val
        return self._request('post',
                             'fifo_command.php?cmd={}%20{}'.format(key,
                                                                   payload))
