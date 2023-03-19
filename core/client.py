import asyncio
import logging
import sys

import httpx

from core.exceptions import TruffleException
from core.protocols import TruffleApp, TruffleRuntime, TruffleEvent


class TruffleClient:
    api_key: str
    __truffle_app: TruffleApp
    __truffle_runtime: TruffleRuntime

    def __init__(self, name: str, phase: str, api_key: str, loop: asyncio.AbstractEventLoop = None):
        self.events: asyncio.Queue[TruffleEvent] = asyncio.Queue(maxsize=10)
        self.logger = logging.getLogger(__name__)
        self.truffle_app = TruffleApp(name, phase)
        self.api_key = api_key
        self.truffle_runtime = TruffleRuntime(
            name="Python", version=f"{sys.version_info.major}.{sys.version_info.minor}"
        )
        self.client = httpx.AsyncClient(
            base_url="https://truffle-api.wafflestudio.com", headers={"x-api-key": self.api_key}
        )
        self.loop = loop or asyncio.get_event_loop()
        self.task = self.loop.create_task(self.send_events())

    async def send_event(self, exc: Exception):
        await self.events.put(
            TruffleEvent(
                app=self.__truffle_app,
                runtime=self.__truffle_runtime,
                exception=TruffleException.of(exc)
            )
        )

    async def send_events(self):
        while True:
            try:
                event = self.events.get_nowait()
                await self.client.post("/events", json=event.__dict__)
            except asyncio.QueueEmpty:
                continue
            except Exception:
                self.logger.warning("Failed to send events to Truffle API", exc_info=True)
