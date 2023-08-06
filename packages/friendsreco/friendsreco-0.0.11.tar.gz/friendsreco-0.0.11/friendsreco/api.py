from aioneo4j import Neo4j

from .controller import Controller
from .repository import Repository
from .service import Service


class Api:
    c: Controller
    controller: Controller
    _neo4j_client: Neo4j
    _repository: Repository
    _service: Service

    def __init__(self, neo4j_url: str, initial_friendships: bool):
        self._neo4j_client = Neo4j(neo4j_url)
        self._repository = Repository(self._neo4j_client)
        self._service = Service(self._repository, initial_friendships)
        self.c = self.controller = Controller(self._service)

    async def start(self):
        await self._service.start()

    async def cleanup(self):
        await self._repository.close()
