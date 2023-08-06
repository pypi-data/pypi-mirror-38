import asyncio
import csv
import logging
import os
from typing import ClassVar, Dict, Iterable, List, Optional

from aioneo4j import Neo4j
from aioneo4j.errors import ClientError
from aioneo4j.errors import Error as Neo4jError

from .domain import Friendships, Recommendations
from .exceptions import Neo4jClientError


class Repository:

    queries_map: ClassVar[Dict[str, str]] = {}
    _neo4j_client: Neo4j
    _root_dir: str
    _cypher_dir: str
    _data_dir: str
    _logger: logging.Logger

    def __init__(self, neo4j_client: Neo4j):
        self._neo4j_client = neo4j_client
        self._root_dir = os.path.dirname(os.path.abspath(__file__))
        self._cypher_dir = os.path.join(self._root_dir, 'cypher')
        self._data_dir = os.path.join(self._root_dir, 'data')
        self._logger = logging.getLogger('friendsreco.repository')

    async def make_friendship(self, person: str, friend: str) -> dict:
        return await self._execute_query('make_friendship',
                                         person=person,
                                         friend=friend)

    async def make_friendships(self, friendships: Iterable[List[str]]) -> List[dict]:
        return [await self.make_friendship(person, friend)
                for person, friend in friendships]

    async def _execute_query(self, filename: str, **kwargs) -> dict:
        query = self._get_cypher_query(filename, **kwargs)

        try:
            self._logger.debug(f'Contents of query {filename}: {query}')
            result = await self._neo4j_client.cypher(query)
            self._logger.debug(f'Results of query {filename}: {result}')
            return result

        except Neo4jError as error:
            if isinstance(error, ClientError):
                message = {
                    'status': error.args[0],
                    'message': error.args[1]['message'],
                    'name': error.args[1]['exception']
                }
                raise Neo4jClientError(message)

            raise error

    def _get_cypher_query(self, filename: str, **kwargs) -> str:
        queries_map = type(self).queries_map

        if filename not in queries_map:
            queries_map[filename] = self._load_query_file(filename)

        if kwargs:
            return queries_map[filename].format(**kwargs)

        return queries_map[filename]

    def _load_query_file(self, filename):
        filename = f'{self._cypher_dir}/{filename}.cypher'

        self._logger.info(f'Loading query {filename}')

        with open(filename) as cypher:
            return cypher.read()

    async def compute_recommendations(self):
        await self._execute_query('compute_recommendations')

    async def get_recommendations(self) -> Iterable[Recommendations]:
        result = await self._execute_query('get_recommendations')
        return (self._get_recommendations(data) for data in result['data'])

    def _get_recommendations(self, reco_data: list) -> Recommendations:
        return Recommendations(reco_data[0], reco_data[1])

    async def get_person_recommendations(self, person_name: str) -> Optional[Recommendations]:
        result = await self._execute_query('get_person_recommendations',
                                           name=person_name)

        if result['data']:
            return self._get_recommendations(result['data'][0])

        return None

    async def close(self):
        await self._neo4j_client.close()

    def get_initial_friendships_data(self) -> Iterable[List[str]]:
        csvfile = open(f'{self._data_dir}/friendships.csv')
        return csv.reader(csvfile, dialect='unix')

    async def get_friendships(self, who: List[str]) -> Iterable[Friendships]:
        if who:
            coros = [self._execute_query('get_person_friendships', name=p) for p in who]
            friendships = await asyncio.gather(*coros)

            return (Friendships(f['data'][0][0], f['data'][0][1]) for f in friendships if f['data'])

        result = await self._execute_query('get_friendships')
        return (Friendships(data[0], data[1]) for data in result['data'])
