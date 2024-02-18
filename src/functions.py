import json
from firebase_admin import db
from config import databaseURL


def fetchData(path, cache):
    ref = db.reference(path=path, url=databaseURL)
    with open("data/etagCache.json", "r") as f:
        etagCache = json.load(f)[cache]
    if not etagCache:
        rawData, etag = ref.get(etag=True)
        with open("data/etagCache.json", "w") as f:
            jsonData = {
                cache: {
                    "etag": etag,
                    "json": rawData,
                }
            }
            json.dump(jsonData, f, indent=4)
    else:
        tupleData = ref.get_if_changed(etag=etagCache["etag"])
        if tupleData[0]:
            rawData = tupleData[1]
            etag = tupleData[2]
            with open("data/etagCache.json", "w") as f:
                jsonData = {
                    cache: {
                        "etag": etag,
                        "json": rawData,
                    }
                }
                json.dump(jsonData, f, indent=4)
        else:
            rawData = etagCache["json"]
    return rawData
