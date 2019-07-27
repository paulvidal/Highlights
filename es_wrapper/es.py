import sys
from pprint import pprint

from elasticsearch import Elasticsearch

# https://elastic:yUt9RjyEdRDBhYe7QYaBGLmb@f04c5f196f37422fbc48aa9f0b4654f6.eu-west-1.aws.found.io:9243

def get_connection():
    """Connect to ES and return a connection
    """
    try:
        es = Elasticsearch(
            ['https://f04c5f196f37422fbc48aa9f0b4654f6.eu-west-1.aws.found.io'],
            http_auth=('elastic', 'yUt9RjyEdRDBhYe7QYaBGLmb'),
            port=9243,
        )
        print("Connected", es.info())

        return es

    except Exception as ex:
        print("Error connecting :", ex)

        sys.exit(1)


def list_indices(es):
    """List ES indices
    """
    return list(es.indices.get('*').keys())


def create_index(es):
    # Create index
    request_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },

        'mappings': {
            'properties': {
                'name': {'type': 'text'}
            }
        }
    }

    print("Creating 'test' index")
    print(es.indices.create(index='test', body=request_body))


# MAIN

es = get_connection()

# Print es indices
print(list_indices(es))

# doc = {
#     'name': 'chelsea',
# }
#
# res = es.index(index="test", id=1, body=doc)
# print(res)

res = es.search(index="test", body={"query": {"fuzzy": {"name": { "value": "chels", "fuzziness": 2 }}}})
print(pprint(res))