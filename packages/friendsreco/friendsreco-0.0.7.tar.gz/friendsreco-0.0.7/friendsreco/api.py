from aioneo4j import Neo4j

from .controller import Controller
from .repository import Repository
from .service import Service


class Api:

    def __init__(self, neo4j_url, initial_friendships):
        self._neo4j_client = Neo4j(neo4j_url)
        self._repository = Repository(self._neo4j_client)
        self._service = Service(self._repository, initial_friendships)
        self.c = self.controller = Controller(self._service)

    async def start(self):
        await self._service.start()

    async def cleanup(self):
        await self._repository.close()
