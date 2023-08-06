import csv
import logging
import os

from aioneo4j import Neo4j
from aioneo4j.errors import Error as Neo4jError, ClientError


class Repository:

    queries_map = {}

    def __init__(self, neo4j_url):
        self._neo4j_client = Neo4j(neo4j_url)
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
            return await self._neo4j_client.cypher(query)

        except Neo4jError as error:
            if isinstance(error, ClientError):
                message = {
                    'status': error.args[0],
                    'message': error.args[1]['message'],
                    'name': error.args[1]['exception']
                }
            else:
                message = {'message': str(error), 'name': type(error).__name__}

            self._logger.error(message)
            raise error

    def _get_cypher_query(self, filename, **kwargs):
        queries_map = type(self).queries_map

        if filename not in queries_map:
            query = queries_map[filename] = self._load_query_file(filename)
        else:
            query = queries_map[filename]

        if kwargs:
            query = queries_map[filename].format(**kwargs)

        self._logger.debug(
            f'Contents of query {filename}: {queries_map[filename]}'
        )
        return query

    def _load_query_file(self, filename):
        filename = f'{self._cypher_dir}/{filename}.cypher'

        self._logger.info(f'Loading query {filename}')

        with open(filename) as cypher:
            return cypher.read()

    def compute_recommendations(self):
        return self._execute_query('compute_recommendations')

    def get_recommendations(self):
        return self._execute_query('get_recommendations')

    def get_person_recommendations(self, person_name):
        return self._execute_query('get_person_recommendations',
                                   name=person_name)

    def close(self):
        return self._neo4j_client.close()

    def get_initial_friendships_data(self):
        csvfile = open(f'{self._data_dir}/friendships.csv')
        return csv.reader(csvfile, dialect='unix')
