import orjson
from bson.objectid import ObjectId
from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel

from utils.utils import raise_bad_request, raise_not_found, raise_server_error


def delete_empty_keys(data: Any):
    """Build dictionary copy sans empty fields"""
    # Remove empty field from dict
    # https://stackoverflow.com/questions/5844672/delete-an-element-from-a-dictionary#5844700
    dic = data.dict()
    # if isinstance(data, BaseModel):
        # dic = **data.dict()
    return { i:dic[i] for i in dic if dic[i] != None }


def is_empty_list_or_dict(o):
    """Check if object is a list or a dict and if it is empty"""
    return (isinstance(o, list) or isinstance(o, dict)) and len(o) == 0


def default_cast(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError


def serialize_mongo_result(doc):
    return orjson.loads( orjson.dumps(doc, default=default_cast) )


def fields_in_create(obj: Any):
    """Build dictionary for data insert by adding createdAt field"""
    if isinstance(obj, BaseModel):
        return { **obj.dict(), "createdAt": datetime.utcnow(), "updatedAt": None}
    else:
        return { **obj, "createdAt": datetime.utcnow(), "updatedAt": None}
    pass


def fields_in_update(obj: Any):
    """Build dictionary for data update by setting updatedAt field"""
    if isinstance(obj, BaseModel):
        return { **obj.dict(), "updatedAt": datetime.utcnow()}
    else:
        return { **obj, "updatedAt": datetime.utcnow()}
    pass


def create_slim_projection(dic: Dict):
    """Create clean MongoDB projection, to save bandwidth"""
    projection = {}
    for k in dic:
        if not is_empty_list_or_dict(dic[k]):
            projection[k] = True
    return projection

#
