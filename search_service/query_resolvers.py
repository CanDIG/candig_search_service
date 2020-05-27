from typing import Any, Dict, List, Optional

import requests
from tartiflette import Resolver

from search_service.backend import (
    query_htsget_service,
    query_metadata_service
)


@Resolver("Query.patients")
async def resolve_query_patients(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> List[Dict[str, Any]]:

    return await query_metadata_service(ctx, 'patients')


@Resolver("Query.samples")
async def resolve_query_samples(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> List[Dict[str, Any]]:

    return await query_metadata_service(ctx, 'samples')


# Note: Nested objects provided by the metadata service do
# no need any further resolving, thus it's moot to declare this:
# @Resolver("Patient.samples")


@Resolver("Sample.sampleUrls")
async def resolve_query_sample_sampleurls(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> List[Dict[str, Any]]:

    return await query_htsget_service(parent)
