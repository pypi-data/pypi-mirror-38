from aiohttp.web import Response
import ujson

class Api:

    def get_recommendations(self):
        return Response(body=ujson.dumps([{
            'person': {'name': 'Test'},
            'suggested_friends': [{'name': 'Test2'}]
        }]))
