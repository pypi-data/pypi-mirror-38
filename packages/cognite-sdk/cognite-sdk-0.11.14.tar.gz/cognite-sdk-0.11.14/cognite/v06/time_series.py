"Timeseries Module\n\nThis module mirrors the Timeseries API. It allows you to fetch data from the api and output it in various formats.\n\nhttps://doc.cognitedata.com/0.6/#Cognite-API-Time-series\n"
from cognite import _utils, config
from cognite.v05.dto import TimeSeriesResponse


def get_time_series_by_id(id, include_metadata=False, **kwargs):
    "Returns a TimeseriesResponse object containing the requested timeseries.\n\n    Args:\n        id (int):           ID of timeseries to look up\n\n        include_metadata (bool):    Decide if the metadata field should be returned or not. Defaults to False.\n\n    Keyword Arguments:\n        api_key (str):          Your api-key.\n\n        project (str):          Project name.\n\n    Returns:\n        v05.dto.TimeSeriesResponse: A data object containing the requested timeseries.\n    "
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.6/projects/{}/timeseries/{}".format(project, id)
    headers = {"api-key": api_key, "accept": "application/json"}
    params = {"includeMetadata": include_metadata}
    res = _utils.get_request(url=url, headers=headers, params=params, cookies=config.get_cookies())
    return TimeSeriesResponse(res.json())


def get_multiple_time_series_by_id(ids, include_metadata=False, **kwargs):
    "Returns a TimeseriesResponse object containing the requested timeseries.\n\n    Args:\n        ids (List[int]):           IDs of timeseries to look up\n\n    Keyword Arguments:\n        api_key (str):          Your api-key.\n        project (str):          Project name.\n\n    Returns:\n        v05.dto.TimeSeriesResponse: A data object containing the requested timeseries with several getter methods with different\n        output formats.\n    "
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.6/projects/{}/timeseries/byids".format(project)
    headers = {"api-key": api_key, "accept": "application/json", "content-type": "application/json"}
    body = {"items": ids}
    params = {"includeMetadata": include_metadata}
    res = _utils.post_request(url=url, body=body, params=params, headers=headers, cookies=config.get_cookies())
    return TimeSeriesResponse(res.json())


def search_for_time_series(
    name=None,
    description=None,
    query=None,
    unit=None,
    is_string=None,
    is_step=None,
    metadata=None,
    asset_ids=None,
    asset_subtrees=None,
    min_created_time=None,
    max_created_time=None,
    min_last_updated_time=None,
    max_last_updated_time=None,
    **kwargs
):
    'Returns a TimeSeriesResponse object containing the search results.\n\n    Args:\n        name (str): Prefix and fuzzy search on name.\n        description (str):  Prefix and fuzzy search on description.\n        query (str):    Search on name and description using wildcard search on each of the words (separated by spaces).\n                        Retrieves results where at least on word must match. Example: "some other"\n        unit (str): Filter on unit (case-sensitive)\n        is_string (bool): Filter on whether the ts is a string ts or not.\n        is_step (bool): Filter on whether the ts is a step ts or not.\n        metadata (Dict):    Filter out time series that do not match these metadata fields and values (case-sensitive).\n                            Format is {"key1": "val1", "key2", "val2"}\n        asset_ids (List): Filter out time series that are not linked to any of these assets. Format is [12,345,6,7890].\n        asset_subtrees (List):  Filter out time series that are not linked to assets in the subtree rooted at these assets.\n                                Format is [12,345,6,7890].\n        min_created_time (int):   Filter out time series with createdTime before this. Format is milliseconds since epoch.\n        max_created_time (int):   Filter out time series with createdTime after this. Format is milliseconds since epoch.\n        min_last_updated_time (int): Filter out time series with lastUpdatedTime before this. Format is milliseconds since epoch.\n        max_last_updated_time (int): Filter out time series with lastUpdatedTime after this. Format is milliseconds since epoch.\n\n    Keyword Arguments:\n        api_key (str):  Your api-key.\n        project (str):  Project name.\n        sort (str):     "createdTime" or "lastUpdatedTime". Field to be sorted.\n                        If not specified, results are sorted by relevance score.\n        dir (str):      "asc" or "desc". Only applicable if sort is specified. Default \'desc\'.\n        limit (int):    Return up to this many results. Maximum is 1000. Default is 25.\n        offset (int):   Offset from the first result. Sum of limit and offset must not exceed 1000. Default is 0.\n        boost_name (bool): Whether or not boosting name field. This option is experimental and can be changed.\n\n    Returns:\n        v05.dto.TimeSeriesResponse: A data object containing the requested timeseries with several getter methods with different\n        output formats.\n    '
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.6/projects/{}/timeseries/search".format(project)
    headers = {"api-key": api_key, "accept": "application/json", "content-type": "application/json"}
    params = {
        "name": name,
        "description": description,
        "query": query,
        "unit": unit,
        "isString": is_string,
        "isStep": is_step,
        "metadata": (str(metadata) if (metadata is not None) else None),
        "assetIds": (str(asset_ids) if (asset_ids is not None) else None),
        "assetSubtrees": (str(asset_subtrees) if (asset_subtrees is not None) else None),
        "minCreatedTime": min_created_time,
        "maxCreatedTime": max_created_time,
        "minLastUpdatedTime": min_last_updated_time,
        "maxLastUpdatedTime": max_last_updated_time,
        "sort": kwargs.get("sort"),
        "dir": kwargs.get("dir"),
        "limit": kwargs.get("limit"),
        "offset": kwargs.get("offset"),
        "boostName": kwargs.get("boost_name"),
    }
    res = _utils.get_request(url, params=params, headers=headers)
    return TimeSeriesResponse(res.json())
