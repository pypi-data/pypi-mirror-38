import asyncio
import logging
from . import formatting
from asynciomeasures.clients.bases import Client
from asynciomeasures.collectors import Collector
from asynciomeasures.reporters import StatsDReporter
from random import random


class StatsD(Client):

    def __init__(self, addr, *, prefix=None, tags=None, loop=None):
        """Sends statistics to the stats daemon over UDP

        Parameters:
            addr (str): the address in the form udp://host:port
            loop (EventLoop): the event loop
            prefix (str): prefix for all keys
            tags (dict): default tags for everything
        """
        self.loop = loop or asyncio.get_event_loop()
        self.log = logging.getLogger(__name__)
        self.prefix = prefix
        self.tags = tags
        self.collector = Collector([], 5000)
        self.reporter = StatsDReporter(addr, loop=self.loop)

    def register(self, metric):
        self.collector.append(metric)
        asyncio.Task(self.send(), loop=self.loop)
        # self.loop.async(self.send())
        return metric

    def format(self, obj):
        return formatting.format(obj, self.prefix, self.tags)

    async def send(self):
        """Sends key/value pairs to StatsD Server.
        """
        await self.reporter.connect()
        rate = random()
        formatter = self.format
        metrics = self.collector.flush(rate=rate, formatter=formatter)
        await self.reporter.send(metrics)

    def close(self):
        self.reporter.close()
