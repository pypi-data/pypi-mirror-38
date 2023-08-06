import logging
from typing import Iterable, List, Optional

from .domain import Friendships, Recommendations
from .repository import Repository


class Service:
    _repository: Repository
    _make_initial_friendships: bool
    _logger: logging.Logger

    def __init__(self, repository: Repository, make_initial_friendships: bool):
        self._repository = repository
        self._make_initial_friendships = make_initial_friendships
        self._logger = logging.getLogger('friendsreco.service')

    async def start(self) -> bool:
        if self._make_initial_friendships:
            self._logger.info('Making initial friendships')
            friendships = self._repository.get_initial_friendships_data()
            await self._repository.make_friendships(friendships)
            return True

        return False

    async def compute_recommendations(self):
        self._logger.info('Computing recommendations')
        await self._repository.compute_recommendations()

    async def get_recommendations(self) -> Iterable[Recommendations]:
        self._logger.info('getting recommendations')
        return await self._repository.get_recommendations()

    async def get_person_recommendations(self, name: str) -> Optional[Recommendations]:
        self._logger.info(f'getting {name} recommendations')
        return await self._repository.get_person_recommendations(name)

    async def get_friendships(self, who: List[str] = []) -> Iterable[Friendships]:
        self._logger.info(f"getting friendships of {', '.join(who)}")
        return await self._repository.get_friendships(who)
