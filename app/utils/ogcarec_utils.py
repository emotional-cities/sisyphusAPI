def validate(id: str, jsonfile: dict):

    try:
        if(jsonfile['id'] != id):
            return {"status":False, "reason": "The document id must match the recordId"}

        ogcareccore = 'http://www.opengis.net/spec/ogcapi-records-1/1.0/req/record-core'

        if(jsonfile['conformsTo'] != ogcareccore and ogcareccore not in jsonfile['conformsTo']):
            return {"status":False, "reason": "The document must comply with OGC API record core 1.0"}

        if(jsonfile['type'] != 'Feature'):
            return {"status":False, "reason": "The document must indicate type Feature."}
    except:
        return {"status":False, "reason": "The document format must conform to OGC API Records Metadata Schema"}

    if 'm' in jsonfile.keys():
        return {"status":False, "reason": "The document cannot contain the m field"}

    if 'geometry' not in jsonfile.keys():
        return {"status":False, "reason": "The document does not contain geometry"}

    if 'properties' not in jsonfile.keys():
        return {"status":False, "reason": "The document does not contain properties"}

    return {"status":True, "reason": None}