from aiohttp.web import Response

import ujson


class Controller:

    def __init__(self, service):
        self._service = service

    async def compute_recommendations(self):
        await self._service.compute_recommendations()
        return Response(status=201)

    async def get_recommendations(self):
        result = await self._service.get_recommendations()
        return Response(text=ujson.dumps(result, indent=2))

    async def get_person_recommendations(self, person_name):
        result = await self._service.get_person_recommendations(person_name)
        return Response(text=ujson.dumps(result, indent=2))
