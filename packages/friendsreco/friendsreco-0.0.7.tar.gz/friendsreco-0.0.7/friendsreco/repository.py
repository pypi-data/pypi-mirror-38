import csv
import logging
import os

from .domain import Recommendations
from .exceptions import Neo4jClientError

from aioneo4j.errors import ClientError
from aioneo4j.errors import Error as Neo4jError


class Repository:

    queries_map = {}

    def __init__(self, neo4j_client):
        self._neo4j_client = neo4j_client
        self._root_dir = os.path.dirname(os.path.abspath(__file__))
        self._cypher_dir = os.path.join(self._root_dir, 'cypher')
        self._data_dir = os.path.join(self._root_dir, 'data')
        self._logger = logging.getLogger('friendsreco.repository')

    def make_friendship(self, person, friend):
        return self._execute_query('make_friendship',
                                   person=person,
                                   friend=friend)

    async def make_friendships(self, friendships):
        return [await self.make_friendship(person, friend)
                for person, friend in friendships]

    async def _execute_query(self, filename, **kwargs):
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

    def _get_cypher_query(self, filename, **kwargs):
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

    def compute_recommendations(self):
        return self._execute_query('compute_recommendations')

    async def get_recommendations(self):
        result = await self._execute_query('get_recommendations')
        return (self._get_recommendation(data) for data in result['data'])

    def _get_recommendation(self, reco_data):
        return Recommendations(reco_data[0], reco_data[1])

    async def get_person_recommendations(self, person_name):
        result = await self._execute_query('get_person_recommendations',
                                     name=person_name)

        if result['data']:
            return self._get_recommendation(result['data'][0])

        return None

    def close(self):
        return self._neo4j_client.close()

    def get_initial_friendships_data(self):
        csvfile = open(f'{self._data_dir}/friendships.csv')
        return csv.reader(csvfile, dialect='unix')
