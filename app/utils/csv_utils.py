import csv
import json
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
        oarec_array.append(transform(row))

    return oarec_array

def transform(input_data):
    # Initialize output_data with default values
    output_data = {
        "type": "Feature",
        "@version": "1",
        "conformsTo": "http://www.opengis.net/spec/ogcapi-records-1/1.0/req/record-core",
        "properties": {
            "type": "dataset",
            "language": "en",
            "formats": ["HTML", "GeoJSON"]
        }
    }

    # Add metadata from the KV filter
    current_timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
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
    output_data["properties"]["license"] = input_data["license"]
    output_data["properties"]["title"] = input_data["title"]
    output_data["properties"]["description"] = input_data["description"]
    output_data["properties"]["keywords"] = input_data["keywords"].split("; ")
    output_data["properties"]["contacts"] = {"name": input_data["contactPoint_name"]}
    output_data["time"] = {
        "resolution": "P1D",
        "interval": json.loads(input_data["temporal_interval"])
    }
    output_data["geometry"] = {
        "coordinates": json.loads(input_data["geometry_coordinates"]),
        "type": "Polygon"
    }
    output_data["links"] = [
        {
            "type": "application/json",
            "rel": "root",
            "title": "The landing page of this server as JSON",
            "href": "https://emotional.byteroad.net?f=json"
        },
        # ... (you can continue to add more links as needed)
    ]

    # Add associations
    temp_data = {
        "href": f"https://emotional.byteroad.net/collections/masked/items/{input_data['id']}?f=json",
        "rel": "item",
        "title": "Link to the feature in JSON format",
        "type": "application/geo+json"
    }
    output_data["properties"]["associations"] = [temp_data]

    # Additional data transformation based on the provided Logstash configuration
    # can be added as needed.

    return output_data

