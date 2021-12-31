"""Sample API Client."""
import datetime
import logging
import asyncio
import socket
from typing import Optional, OrderedDict
import aiohttp
import async_timeout
import json
import os

TIMEOUT = 10


_LOGGER: logging.Logger = logging.getLogger(__name__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class CalendarApiClient:
    def __init__(self, entry_id: str) -> None:
        """Sample API Client."""
        self.entry_id = entry_id
        self.data = {}

    async def async_get_data(self) -> dict:
        """Get data from the API."""
        # url = "http://my-json-server.typicode.com/alexandre2297/rest_api/posts/1"
        data = open(os.path.join(ROOT_DIR, "data.json"), "r")
        self.data = json.load(data)

        # On first load, create entry_id data struct in db
        if self.entry_id not in self.data:
            self.data[self.entry_id] = {"events": []}

        return self.data[self.entry_id]

    async def save(self):
        with open(os.path.join(ROOT_DIR, "data.json"), "w") as outfile:
            json.dump(self.data, outfile)

    async def get_next_event(self, entry_id):
        # print(self.data[entry_id]["events"])
        return None

    async def add_event(
        self,
        event: str,
        start: str,
        start_time: str = "",
        end: str = "",
        end_time: str = "",
    ):
        if end == "":
            end = start

        if end_time == "":
            end_time = start_time

        new_event = {
            "summary": event,
            "start": (
                {"date": start}
                if start_time == ""
                else {"dateTime": start + " " + start_time}
            ),
            "end": (
                {"date": end} if end_time == "" else {"dateTime": end + " " + end_time}
            ),
        }

        self.data[self.entry_id]["events"].append(new_event)

        self.data[self.entry_id]["events"].sort(
            key=lambda event: (
                datetime.datetime.strptime(event["start"]["date"], "%Y-%m-%d 00:00:00")
                if "date" in event["start"]
                else datetime.datetime.strptime(
                    event["start"]["dateTime"], "%Y-%m-%d %H:%M:%S"
                )
            )
        )

        await self.save()
        return self.data
