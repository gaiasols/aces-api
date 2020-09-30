import logging
from datetime import datetime
from random import shuffle
from time import time
from typing import Any, List

from pymongo import ReturnDocument

from core.config import DOCTYPE_EV_GPQ
from crud.utils import (
    delete_empty_keys,
    fields_in_create,
    fields_in_update,
    raise_bad_request,
    raise_not_found,
    raise_server_error,
)
from db.mongo import get_collection
from models.ev.gpq import GPQEvidence, GPQEvidenceCreate, GPQRow, GPQRowUpdate




async def find_one(
    projectId: str,
    personaId: str
) -> GPQEvidence:
    logging.info(">>> " + __name__ + ":find_one")

    collection = get_collection(DOCTYPE_EV_GPQ)
    return await collection.find_one({
        "projectId": projectId,
        "personaId": personaId
    })


async def create_doc(
    license: str,
    projectId: str,
    personaId: str,
    fullname: str
) -> GPQEvidence:
    logging.info(">>> " + __name__ + ":create_doc")

    # Check item numbers from project
    # Assume it is 30
    items = 30
    # Per item = 3 minutes
    maxTime = items * 3 * 60 * 1000
    seqs = [i for i in range(1, items + 1)]
    shuffle(seqs)
    strSeqs = ' '.join(map(str, seqs))
    logging.info(strSeqs)
    model = GPQEvidenceCreate(
        license = license,
        projectId = projectId,
        personaId = personaId,
        fullname = fullname,
        items = items,
        maxTime = maxTime,
        sequence = strSeqs
    )
    props = fields_in_create(model)
    try:
        collection = get_collection(DOCTYPE_EV_GPQ)
        rs = await collection.insert_one(props)
        if rs.inserted_id:
            return await collection.find_one({"_id": rs.inserted_id})
    except Exception as e:
        raise_server_error(str(e.detail))


async def init(projectId: str, personaId: str) -> Any:
    logging.info(">>> " + __name__ + ":init")
    try:
        collection = get_collection(DOCTYPE_EV_GPQ)
        doc = await collection.find_one(
            {"projectId": projectId, "personaId": personaId},
            {"_id": 0, "initiated": 1, "done": 1}
        )

        ts = round(time() * 1000)
        now = datetime.utcnow()
        props = {"initiated": ts, "touched": ts, "updatedAt": now}
        # It it's already initiated, just touch.
        if doc and doc["initiated"]:
            props = {"touched": ts, "updatedAt": now}
        rs = await collection.find_one_and_update(
            {"projectId": projectId, "personaId": personaId},
            {"$set": props},
            {"_id": 0, "touched": 1},
            return_document=ReturnDocument.AFTER
        )

        if doc["done"] > 0:
            return {"touched": rs["touched"], "next": doc["done"] + 1}
        else:
            return {"touched": rs["touched"], "next": None}
    except Exception as e:
        raise_server_error(str(e))


async def start(projectId: str, personaId: str) -> Any:
    logging.info(">>> " + __name__ + ":start")
    try:
        collection = get_collection(DOCTYPE_EV_GPQ)
        ts = round(time() * 1000)
        now = datetime.utcnow()
        props = {"started": ts, "touched": ts, "updatedAt": now}
        rs = await collection.find_one_and_update(
            {"projectId": projectId, "personaId": personaId},
            {"$set": props},
            {"_id": 0, "touched": 1},
            return_document=ReturnDocument.AFTER
        )
        logging.info(rs)
        return {"touched": rs["touched"], "next": 1}
    except Exception as e:
        raise_server_error(str(e))

# seq: int
# wbSeq: int
# element: str
# statement: str
# lastTouch: int
async def update_row(
    projectId: str,
    personaId: str,
    data: GPQRowUpdate
) -> Any:
    logging.info(">>> " + __name__ + ":update_row")
    try:
        collection = get_collection(DOCTYPE_EV_GPQ)
        ts = round(time() * 1000)
        now = datetime.utcnow()
        elapsed = ts - data.lastTouch
        model = GPQRow(
            **data.dict(),
            saved = ts,
            elapsed = ts - data.lastTouch
        )
        props = {"done": data.seq, "touched": ts, "updatedAt": now}
        if data.seq == data.total:
            props["finished"] = ts
        rs = await collection.find_one_and_update(
            {"projectId": projectId, "personaId": personaId},
            {
                "$set": props,
                "$inc": {"netTime": elapsed, "remains": -elapsed},
                "$push": {"rows": model.dict()}
            },
            {"_id": 0, "touched": 1},
            return_document=ReturnDocument.AFTER
        )
        logging.info(rs)
        if data.seq < data.total:
            return {"touched": rs["touched"], "next": data.seq + 1}
        else:
            return {"touched": rs["touched"], "next": None}
        return rs
    except Exception as e:
        raise_server_error(str(e))
