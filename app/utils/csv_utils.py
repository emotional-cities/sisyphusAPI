import csv
import json
import re
from app.schemas.recordgeojson import RecordGeoJSON, Theme, Concept
from datetime import datetime

def csv_to_json(csv_file_content):
    """Convert a CSV file to an array of JSON documents."""
    json_array = []

    csv_reader = csv.DictReader(csv_file_content, delimiter='|')

    for row in csv_reader:
        json_array.append(row)

    return json_array

def csv_to_oarec(csv_file_content):
    json_array = csv_to_json(csv_file_content)

    oarec_array = []

    for row in json_array:
        try:
            oarec_array.append(transform(row))
        except Exception as e:
            raise e

    return oarec_array

def remove_nulls(d):
    return {k: v for k, v in d.items() if v is not None}

def process_comma_separated_string(s):
    separator = ',' if ',' in s else ';'
    return [item.strip().lower() for item in s.split(separator)]

def contains_url(s):
    # This is a basic pattern for matching URLs. You can use more complex patterns if needed.
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    
    if url_pattern.search(s):
        return True
    else:
        return False

def transform(input_data):
    # Initialize output_data with default values
    output_data = {
        "type": "Feature",
        "@version": "1",
        "conformsTo": [ 
            "http://www.opengis.net/spec/ogcapi-records-1/1.0/req/record-core" 
            ],
        "properties": {
            "type": "dataset",
            "language": {
                "code": "en",
                "name": "English"
            },
            "formats": ["HTML", "GeoJSON"],
            "themes": []
        }
    }

    # Add metadata from the KV filter
    current_timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    output_data["recordCreated"] = current_timestamp
    output_data["recordUpdated"] = current_timestamp
    output_data["@timestamp"] = current_timestamp
    output_data["properties"]["created"] = current_timestamp
    output_data["properties"]["updated"] = current_timestamp
    output_data["properties"]["title"] = "TBD"
    output_data["properties"]["description"] = "TBD"
    output_data["properties"]["publisher"] = "https://byteroad.net/"
    output_data["properties"]["contactPoint"] = "Byte Road"

    # Add fields directly from the input JSON
    output_data["id"] = input_data["id"]
    record_id = input_data["id"]

    if(input_data["license"]):
        output_data["properties"]["license"] = input_data["license"]
    else:
        output_data["properties"]["license"] = "other"
    output_data["properties"]["title"] = input_data["title"]
    output_data["properties"]["description"] = input_data["description"]
    output_data["properties"]["keywords"] = process_comma_separated_string(input_data["keywords"])
    themes = process_comma_separated_string(input_data["themes"])
    output_data["properties"]["themes"] = []
    themes_index = 0
    for row in themes:
        if(row > ''):
            if(len(output_data["properties"]["themes"]) <= themes_index):
                output_data["properties"]["themes"].append({"scheme" : 'https://www.eionet.europa.eu/gemet/en/themes/', "concepts" : []})
            if(contains_url(row)):
                output_data["properties"]["themes"][themes_index]["concepts"].append({"id" : "", "url" : row})
            else:
                output_data["properties"]["themes"][themes_index]["concepts"].append({"id" : row})
            themes_index += 1

    output_data["properties"]["contacts"] = [{"name": input_data["contactPoint_name"]}]
    if(input_data["temporal_interval"] and input_data["temporal_interval"] > ''):
        output_data["time"] = {
            "resolution": "P1D",
            "interval": json.loads(input_data["temporal_interval"])
        }
    else:
        output_data["time"] = {}

    output_data["geometry"] = {
        "coordinates": json.loads(input_data["geometry_coordinates"]),
        "type": "Polygon"
    }
    if(input_data["public"] == "YES"):
        output_data["links"] = [
            {
                "type": "application/json",
                "rel": "root",
                "title": "The landing page of this server as JSON",
                "href": "https://emotional.byteroad.net?f=json"
            },
            {
                "type": "application/json",
                "rel": "self",
                "title": "This document as JSON",
                "href": "https://emotional.byteroad.net/collections/ec_catalog/%s?f=json" % record_id
            },
            {
                "href": "https://emotional.byteroad.net/collections/%s?f=json" % record_id,
                "rel": "item",
                "title": "OGC API Features for %s" % record_id,
                "type": "application/geo+json"
            },
            {
                "href": "https://emotional.byteroad.net/collections/%s/tiles?f=json" % record_id,
                "rel": "item",
                "title": "OGC API Tiles for %s" % record_id,
                "type": "application/geo+json"
            },
            {
                "href": "https://emotional.byteroad.net/sisyphus/api/v1/dataset/%s?f=geojson" % record_id,
                "rel": "item",
                "title": "GeoJson download link for %s" % record_id,
                "type": "application/geo+json"
            },
            {
                "href": "https://emotional.byteroad.net/sisyphus/api/v1/dataset/%s?f=geoparquet" %  record_id,
                "rel": "item",
                "title": "GeoParquet download link for %s" % record_id,
                "type": "application/vnd.apache.parquet"
            },
            {
                "href": "https://emotional.byteroad.net/sisyphus/api/v1/dataset/%s?f=geopackage" % record_id,
                "rel": "item",
                "title": "GeoPackage download link for %s" % record_id,
                "type": "application/x-sqlite3"
            },
            {
                "rel": "item",
                "type": "image/png",
                "title": "OGC Web Map Service (WMS)",
                "href": "https://emotional.byteroad.net/geoserver/ows?service=WMS&version=1.3.0&request=GetMap&crs={crs}&bbox={bbox}&layers=" + record_id + "&width={width}&height={height}&format=image/png",
                "templated": True,
                "variables": {
                    "crs": {
                    "description": "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
                    "type": "string",
                    "enum": [
                        "EPSG:4326"
                    ]
                    },
                    "bbox": {
                    "description": "...",
                    "type": "array",
                    "items": {
                        "type": "number",
                        "format": "double"
                    },
                    "minItems": 4,
                    "maxItems": 4
                    },
                    "width": {
                    "description": "...",
                    "type": "number",
                    "format": "integer",
                    "minimum": 600,
                    "maximum": 5000
                    },
                    "height": {
                    "description": "...",
                    "type": "number",
                    "format": "integer",
                    "minimum": 600,
                    "maximum": 5000
                    }
                }
            }
        ]
    else:
        output_data["links"] = [
            {
                "type": "application/json",
                "rel": "root",
                "title": "The landing page of this server as JSON",
                "href": "https://emotional.byteroad.net?f=json"
            },
            {
                "type": "application/json",
                "rel": "self",
                "title": "This document as JSON",
                "href": "https://emotional.byteroad.net/collections/ec_catalog/%s?f=json" % record_id
            }
        ]

    # Is there a way to optimize this?
    return json.loads(RecordGeoJSON.from_json(json.dumps(output_data)).to_json(), object_hook=remove_nulls)
