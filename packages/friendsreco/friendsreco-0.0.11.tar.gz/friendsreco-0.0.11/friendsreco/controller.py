from typing import List

from aiohttp.web import Response

import ujson
from friendsreco.service import Service


class Controller:
    _service: Service

    def __init__(self, service: Service):
        self._service = service

    async def compute_recommendations(self) -> Response:
        await self._service.compute_recommendations()
        return Response(status=201)

    async def get_recommendations(self) -> Response:
        result = await self._service.get_recommendations()
        return Response(text=ujson.dumps(result, indent=2))

    async def get_person_recommendations(self, person_name: str) -> Response:
        result = await self._service.get_person_recommendations(person_name)
        return Response(text=ujson.dumps(result, indent=2))

    async def get_friendships(self, who: List[str] = []) -> Response:
        result = await self._service.get_friendships(who)
        return Response(text=ujson.dumps(result, indent=2))
