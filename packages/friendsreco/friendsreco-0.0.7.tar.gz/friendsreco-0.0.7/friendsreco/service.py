import logging


class Service:
    def __init__(self, repository, make_initial_friendships):
        self._repository = repository
        self._make_initial_friendships = make_initial_friendships
        self._logger = logging.getLogger('friendsreco.service')

    async def start(self):
        if self._make_initial_friendships:
            self._logger.info('Making initial friendships')
            friendships = self._repository.get_initial_friendships_data()
            return await self._repository.make_friendships(friendships)

        return None

    async def compute_recommendations(self):
        self._logger.info('Computing recommendations')
        await self._repository.compute_recommendations()

    def get_recommendations(self):
        self._logger.info('getting recommendations')
        return self._repository.get_recommendations()

    def get_person_recommendations(self, name):
        self._logger.info(f'getting {name} recommendations')
        return self._repository.get_person_recommendations(name)
