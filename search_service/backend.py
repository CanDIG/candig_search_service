import json
import re
import requests

from search_service.config import (
    HTSGET_SERVICE_URL,
    METADATA_SERVICE_URL
)


NON_METADATA_SUBQUERIES = [
    # find the sampleUrls nested object, that is until the next }
    re.compile('sampleUrls[^}]*'),
]


async def sanitize_metadata_query(query):
    """
    Since our GraphQL schema for this application cover multiple
    other graphQL schemas (or simply other data sources) we have
    to do some kind of manual schema stitching. The following is
    fairly ugly but workable fix until we come up with a better
    long term solution
    """
    for regex in NON_METADATA_SUBQUERIES:
        match = regex.search(query)

        if match:
            start, end = match.span()
            query = query[:start] + query[end + 1:]

    return query


async def query_metadata_service(context, object_type):
    url = f"{METADATA_SERVICE_URL}/graphql"

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


async def query_htsget_service(parent):
    if 'sampleId' in parent:
        url = f"{HTSGET_SERVICE_URL}/htsget/v1/variants?id={parent['sampleId']}"
        res = requests.get(url)
        
        if res.status_code == 200:
            return res.json()['htsget']['urls']
        else:
            return [{'url': None}]
    else:
        return [{'url': None}]
