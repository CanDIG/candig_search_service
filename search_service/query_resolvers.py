from typing import Any, Dict, List, Optional

import requests
from tartiflette import Resolver

from search_service.backend import query_metadata_service


@Resolver("Query.patients")
async def resolve_query_patients(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> List[Dict[str, Any]]:
    """
    Resolver in charge of returning all recipes.
    :param parent: initial value filled in to the engine `execute` method
    :param args: computed arguments related to the field
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution
    :type parent: Optional[Any]
    :type args: Dict[str, Any]
    :type ctx: Dict[str, Any]
    :type info: ResolveInfo
    :return: the list of all recipes
    :rtype: List[Dict[str, Any]]
    """
    return await query_metadata_service(ctx, 'patients')


@Resolver("Query.samples")
async def resolve_query_samples(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> List[Dict[str, Any]]:

    return await query_metadata_service(ctx, 'samples')


@Resolver("Patient.samples")
async def resolve_query_patients_samples(
    parent: Optional[Dict[str, Any]],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> Optional[List[Dict[str, Any]]]:

    if 'samples' in parent:
        return parent['samples']
    else:
        return None


@Resolver("Sample.sampleUrls")
async def resolve_query_sample_sampleurls(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> List[Dict[str, Any]]:

    if 'sampleId' in parent:
        url = f"http://0.0.0.0:3000/htsget/v1/variants?id={parent['sampleId']}"
        res = requests.get(url)
        
        if res.status_code == 200:
            return res.json()['htsget']['urls']
        else:
            return [{'url': None}]
    else:
        return [{'url': None}]
