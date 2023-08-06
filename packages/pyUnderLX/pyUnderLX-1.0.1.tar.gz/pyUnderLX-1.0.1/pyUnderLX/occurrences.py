"""Representation of Occurrences."""
import logging
from collections import namedtuple
import aiohttp

from .api import UnderLX
from .consts import METRO_LINES

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Occurrences:
    """Represents occurences."""

    def __init__(self, websession):
        self.api = UnderLX(websession)
     
    @classmethod
    async def get(cls, websession):

        self = Occurrences(websession)
        self.occurrences  = await self.api.ongoing()
        
        return self

    async def ongoing(self):
        """Retrieve ongoing occurences."""

        self.occurrences = await self.api.ongoing()

        return self.occurrences
    
    async def split_per_metroLine(self):
        """function to split the occurrences by Metroline."""
        _occurrence_MetroLine_list = []
        
        for key in METRO_LINES.keys():
            _occurrence_MetroLine = await self.occurrences_in_metroLine(key)
            _occurrence_MetroLine_list.append(_occurrence_MetroLine)

        return _occurrence_MetroLine_list 

    async def occurrences_in_metroLine(self, line):
        """function to return occurrences in a specific Metroline."""
        _occurrences = self.occurrences
        Occurrence_MetroLine = namedtuple('MetroLine', ['line','friendlyName','occurrences'])
        
        _metroLine_occurrences_list = []    
        for o in _occurrences:
            if o.line == line:
                _metroLine_occurrences_list.append(o)
                
        _occurrence_MetroLine = Occurrence_MetroLine(line,METRO_LINES[line],_metroLine_occurrences_list)
        
        return _occurrence_MetroLine

    async def full_list(self):
        """Retrieve ongoing occurrences."""

        return self.occurrences

    async def number_of_occurrences(self, line):
        numOccur = 0
        
        if line == None:
            numOccur = len(self.occurrences)
        else:
            _metroLineOccurrences = await self.occurrences_in_metroLine(line)
            numOccur = len(_metroLineOccurrences.occurrences)
            
        return numOccur

    async def occurrence_status(self, id):
        self.occurrenceStatus  = await self.api.status(id)

        return self.occurrenceStatus
