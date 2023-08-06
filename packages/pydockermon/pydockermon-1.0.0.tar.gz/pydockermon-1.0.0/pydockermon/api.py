"""
API Calls.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import asyncio
import logging
import socket

import aiohttp
import async_timeout

from .const import URL, HEADERS

LOGGER = logging.getLogger(__name__)


class API(object):
    """A class for API calls."""

    def __init__(self, loop, session, host, port,
                 username=None, password=None, ssl=False):
        """Initialize the class."""
        self._loop = loop
        self._session = session
        self._host = host
        self._port = port
        self._ssl = ssl
        self._containers = []
        self._container_metrics = {}
        self._container_states = {}
        if username is None:
            self._auth = None
        else:
            self._auth = aiohttp.BasicAuth(username, password)

    async def api_call(self, endpoint):
        """Get result from API call."""
        schema = 'https' if self._ssl else 'http'
        url = URL.format(schema=schema, host=self._host,
                         port=self._port, endpoint=endpoint)
        api_response = {}
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                if self._auth is None:
                    response = await self._session.get(url, headers=HEADERS)
                else:
                    response = await self._session.get(url,
                                                       auth=self._auth,
                                                       headers=HEADERS)
                data = await response.json()
                api_response = {"success": True,
                                "status_code": response.status,
                                "data": data}
        except (asyncio.TimeoutError,
                aiohttp.ClientError, socket.gaierror) as error:
            LOGGER.error('Error connecting to HA Dockermon, %s', error)
            api_response = {"success": False,
                            "status_code": None,
                            "data": None}
        return api_response

    async def container_state(self, container):
        """Return the state of a container."""
        endpoint = "container/{}".format(container)
        LOGGER.debug("Getting container state %s.", container)
        api_response = await self.api_call(endpoint)
        LOGGER.debug(api_response)
        return api_response

    async def container_metrics(self, container):
        """Return the metrics for a container."""
        endpoint = "container/{}/stats".format(container)
        LOGGER.debug("Getting container metrics %s.", container)
        api_response = await self.api_call(endpoint)
        LOGGER.debug(api_response)
        return api_response

    async def container_start(self, container):
        """Start a spesified container."""
        endpoint = "container/{}/start".format(container)
        LOGGER.debug("Starting %s.", container)
        api_response = await self.api_call(endpoint)
        LOGGER.debug(api_response)
        return api_response

    async def container_stop(self, container):
        """Stop a spesified container."""
        endpoint = "container/{}/stop".format(container)
        LOGGER.debug("Stopping %s.", container)
        api_response = await self.api_call(endpoint)
        LOGGER.debug(api_response)
        return api_response

    async def container_pause(self, container):
        """Pause a spesified container."""
        endpoint = "container/{}/pause".format(container)
        LOGGER.debug("Pausing %s.", container)
        api_response = await self.api_call(endpoint)
        LOGGER.debug(api_response)
        return api_response

    async def container_unpause(self, container):
        """Unpause a spesified container."""
        endpoint = "container/{}/unpause".format(container)
        LOGGER.debug("Unpausing %s.", container)
        api_response = await self.api_call(endpoint)
        return api_response

    async def container_restart(self, container):
        """Restart a spesified container."""
        endpoint = "container/{}/restart".format(container)
        LOGGER.debug("Restarting %s.", container)
        api_response = await self.api_call(endpoint)
        LOGGER.debug(api_response)
        return api_response

    async def list_containers(self):
        """Get a list of all containers."""
        containers = []
        LOGGER.debug("Listing all containers on the host.")
        api_response = await self.api_call('containers')
        if api_response['data'] is not None:
            for container in api_response['data']:
                containers.append(container['Names'][0][1:])
        LOGGER.debug(containers)
        self._containers = {"success": api_response['success'],
                            "status_code": api_response['status_code'],
                            "data": containers}

    async def get_all_container_metrics(self):
        """Get the metrics of all containers."""
        container_metrics = {}
        await self.list_containers()
        if self.all_containers is not None:
            for container in self.all_containers['data']:
                metrics = await self.container_metrics(container)['data']
                container_metrics[container] = metrics
        self._container_metrics = {"success": True,
                                   "status_code": None,
                                   "data": container_metrics}

    async def get_all_container_states(self):
        """Get the state of all containers."""
        container_states = {}
        await self.list_containers()
        if self.all_containers is not None:
            for container in self.all_containers['data']:
                state = await self.container_state(container)
                container_states[container] = state['data']
        self._container_states = {"success": True,
                                  "status_code": None,
                                  "data": container_states}

    @property
    def all_containers(self):
        """Return a list of all containers."""
        return self._containers

    @property
    def all_container_metrics(self):
        """Return metrics for all containers."""
        return self._container_metrics

    @property
    def all_container_states(self):
        """Return the state for all containers."""
        return self._container_states
