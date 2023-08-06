"Sequences Module\n\nThis module mirrors the Sequences API.\n\nhttps://doc.cognitedata.com/api/0.6/#tag/Sequences\n"
import json
from cognite import _utils, config
from cognite.v06.dto import Sequence, SequenceDataRequest, SequenceDataResponse, Row


def post_sequences(sequences, **kwargs):
    "Create a new time series.\n\n    Args:\n        sequences (list[v06.dto.Sequence]):  List of sequence data transfer objects to create.\n\n    Keyword Args:\n        api_key (str):                       Your api-key.\n        project (str):                       Project name.\n\n    Returns:\n        The created sequence\n    "
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.6/projects/{}/sequences".format(project)
    for sequence in sequences:
        del sequence.id
        for column in sequence.columns:
            del column.id
    body = {"items": [sequence.__dict__ for sequence in sequences]}
    headers = {"api-key": api_key, "content-type": "application/json", "accept": "application/json"}
    res = _utils.post_request(url, body=body, headers=headers)
    json_response = json.loads(res.text)
    the_sequence: dict = json_response["data"]["items"][0]
    return Sequence.from_JSON(the_sequence)


def get_sequence_by_id(id, **kwargs):
    "Returns a Sequence object containing the requested sequence.\n\n    Args:\n        id (int):       ID of the sequence to look up\n\n    Keyword Arguments:\n        api_key (str):  Your api-key.\n        project (str):  Project name.\n\n    Returns:\n        v06.dto.Sequence: A data object containing the requested sequence.\n    "
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.6/projects/{}/sequences/{}".format(project, id)
    headers = {"api-key": api_key, "accept": "application/json"}
    res = _utils.get_request(url=url, headers=headers, cookies=config.get_cookies())
    json_response = json.loads(res.text)
    the_sequence: dict = json_response["data"]["items"][0]
    return Sequence.from_JSON(the_sequence)


def get_sequence_by_external_id(external_id, **kwargs):
    "Returns a Sequence object containing the requested sequence.\n\n    Args:\n        external_id (int):  External ID of the sequence to look up\n\n    Keyword Arguments:\n        api_key (str):      Your api-key.\n        project (str):      Project name.\n\n    Returns:\n        v06.dto.Sequence: A data object containing the requested sequence.\n    "
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.6/projects/{}/sequences".format(project)
    headers = {"api-key": api_key, "accept": "application/json"}
    params = {"externalId": external_id}
    res = _utils.get_request(url=url, params=params, headers=headers, cookies=config.get_cookies())
    json_response = json.loads(res.text)
    the_sequence: dict = json_response["data"]["items"][0]
    return Sequence.from_JSON(the_sequence)


def delete_sequence_by_id(id, **kwargs):
    "Deletes the sequence with the given id.\n\n    Args:\n        id (int):       ID of the sequence to delete\n\n    Keyword Arguments:\n        api_key (str):  Your api-key.\n        project (str):  Project name.\n\n    Returns:\n    "
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.6/projects/{}/sequences/{}".format(project, id)
    headers = {"api-key": api_key, "accept": "application/json"}
    res = _utils.delete_request(url=url, headers=headers, cookies=config.get_cookies())
    return res.json()


def post_data_to_sequence(id, rows, **kwargs):
    "Posts data to a sequence.\n\n    Args:\n        id (int):       ID of the sequence.\n        rows (list):    List of rows with the data.\n\n    Keyword Arguments:\n        api_key (str):  Your api-key.\n        project (str):  Project name.\n\n    Returns:\n    "
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.6/projects/{}/sequences/{}/postdata".format(project, id)
    body = {"items": [{"rows": [row.__dict__ for row in rows]}]}
    headers = {"api-key": api_key, "content-type": "application/json", "accept": "application/json"}
    res = _utils.post_request(url, body=body, headers=headers)
    return res.json()


def get_data_from_sequence(id, inclusive_from, inclusive_to, limit=100, column_ids=None, **kwargs):
    "Gets data from the given sequence.\n\n    Args:\n        id (int):                id of the sequence.\n        inclusive_from (int):    Row number to get from (inclusive).\n        inclusive_to (int):      Row number to get to (inclusive).\n        limit (int):             How many rows to return.\n        column_ids (List[int]):  ids of the columns to get data for.\n\n    Keyword Arguments:\n        api_key (str):           Your api-key.\n        project (str):           Project name.\n\n    Returns:\n        v06.dto.Sequence: A data object containing the requested sequence.\n    "
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.6/projects/{}/sequences/{}/getdata".format(project, id)
    headers = {"api-key": api_key, "accept": "application/json", "Content-Type": "application/json"}
    sequenceDataRequest: SequenceDataRequest = SequenceDataRequest(
        inclusive_from=inclusive_from, inclusive_to=inclusive_to, limit=limit, column_ids=(column_ids or [])
    )
    body = {"items": [sequenceDataRequest.__dict__]}
    res = _utils.post_request(url=url, body=body, headers=headers, cookies=config.get_cookies())
    json_response = json.loads(res.text)
    the_data: dict = json_response["data"]["items"][0]
    return SequenceDataResponse.from_JSON(the_data)
