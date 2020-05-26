import json
import re
import requests


NON_METADATA_SUBQUERIES = [
    re.compile('sampleUrls[^}]*'),
]


async def sanitize_metadata_query(query):
    """
    Since our GraphQL schema for this application cover multiple
    other graphQL schemas (or simply other data sources) we have
    to do some kind of manual schema stitching. The following is
    fairly ugly but workable solution until we come up with a better
    long term solution
    """
    for regex in NON_METADATA_SUBQUERIES:
        match = regex.search(query)

        if match:
            start, end = match.span()
            query = query[:start] + query[end + 1:]

    return query


async def query_metadata_service(context, object_type):
    url = 'http://127.0.0.1:8000/graphql'

    json_query = await context['req'].json()
    cleaned_query = await sanitize_metadata_query(json_query['query'])
    json_query['query'] = cleaned_query

    res = requests.post(url, json=json_query)
    res.raise_for_status()
    raw_json = res.json()

    if 'data' in raw_json:
        if object_type in raw_json['data']:
            return raw_json['data'][object_type]
        else:
            raise Exception(f'Could not find {object_type} in response from metadata service')
    else:
        raise Exception('Wrong format in response from metadata service')
