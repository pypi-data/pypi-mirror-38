"""API to UnderLX."""
import logging
from collections import namedtuple
import aiohttp

from .consts import API_ONGOING, API_BASELINE

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


class UnderLX:
    """Interfaces to  https://api.perturbacoes.tny.im/v1/disturbances"""

    def __init__(self, websession):
        self.websession = websession

    async def retrieve(self, url, **kwargs):
        """Issue API requests."""
        try:
            async with self.websession.request('GET', url, **kwargs) as res:
                if res.status != 200:
                    raise Exception("Could not retrieve information from API")
                if res.content_type == 'application/json':
                    return await res.json()
                return await res.text()
        except aiohttp.ClientError as err:
            logging.error(err)

    async def ongoing(self):
        """Retrieve ongoing Occurrences."""

        data = await self.retrieve(API_ONGOING)

        Occurrence = namedtuple('Occurrence', ['id', 'official',
                                         'oStartTime', 'oEndTime',
                                         'oEnded', 'startTime',
                                         'endTime', 'ended',
                                         'description','notes',
                                         'network','line',
                                         'categories','statuses'])
        
#        OStatus = namedtuple('OStatus', ['id', 'time',
#                                         'downtime', 'status',
#                                         'msgType', 'source'] )

        _occurrences = []
        for occurrence in data:

            _occurence = Occurrence(
                occurrence['id'],occurrence['official'],
                occurrence['oStartTime'],occurrence['oEndTime'],
                occurrence['oEnded'],occurrence['startTime'],
                occurrence['endTime'],occurrence['ended'],
                occurrence['description'],occurrence['notes'],
                occurrence['network'],occurrence['line'],
                occurrence['categories'],occurrence['statuses']
                )
            _occurrences.append(_occurence)
       
        return _occurrences

    async def status(self, id):
        """Retrieve status list based on occurrence id."""

        data = await self.retrieve(API_BASELINE + "{id}?omitduplicatestatus=true".
                                   format(id=id))

        return data['statuses']