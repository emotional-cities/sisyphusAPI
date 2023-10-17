import json

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

    recordobjetc = RecordGeoJSON.from_json_string(json.dumps(jsonfile))
    try:
        recordobjetc.validate();
    except ValueError as e:
        return {"status":False, "reason": {e}}

    return {"status":True, "reason": None}

class Link:
    def __init__(self):
        self.href = "http://example.com"
        # Other properties with dummy values
        # self.rel = ""
        # self.type = ""
        # self.hreflang = ""
        # self.title = ""
        # self.templated = False
        # self.variables = {}
        # self.created = "2022-10-11T00:00:00Z"
        # self.updated = "2022-10-11T00:00:00Z"

    def validate(self):
        if not self.href:
            raise ValueError("href is a required field")
        if not self.href.startswith("http://") and not self.href.startswith("https://"):
            raise ValueError("Invalid href format")

    def from_dict(cls, data: dict) -> "Link":
        return cls(
            href=data['href'],
            rel=data.get('rel'),
            type_=data.get('type'),
            hreflang=data.get('hreflang'),
            title=data.get('title'),
            templated=data.get('templated'),
            variables=data.get('variables'),
            created=data.get('created'),
            updated=data.get('updated')
        )


class Time:
    def __init__(self):
        # Dummy initialization for the time object
        self.resolution = "P1D"
        self.interval = "2022-10-11T00:00:00Z"

    def validate(self):
        pass

    def from_dict(cls, data: dict) -> "Time":
        return cls(
            date=data.get('date'),
            timestamp=data.get('timestamp'),
            interval=data.get('interval'),
            resolution=data.get('resolution')
        )


class GeometryGeoJSON:
    def __init__(self):
        # Dummy initialization for the GeometryGeoJSON object
        self.type = "Polygon"
        self.coordinates = [0, 0]

    def validate(self):
        if self.type and self.type not in ["Point", "LineString", "Polygon"]: # and other GeoJSON types
            raise ValueError("Invalid geometry type")

    def from_dict(cls, data: dict) -> "GeometryGeoJSON":
        pass

class Language:
    def __init__(self):
        self.code = "en"

    def validate(self):
        if self.code and len(self.code) != 2:
            raise ValueError("Language code should be 2 characters long")


class Theme:
    def __init__(self):
        self.themeName = "dummy_theme"

    def validate(self):
        if not self.themeName:
            raise ValueError("themeName is a required field")


class Contact:
    def __init__(self):
        self.identifier = "12345"
        self.name = "John Doe"
        self.position = "Manager"
        self.organization = "ACME Inc."
        self.logo = {"rel": "icon", "type": "image/png"}
        self.phones = [{"value": "+14165550142"}]
        self.emails = [{"value": "johndoe@example.com"}]
        self.addresses = []
        self.links = [Link()]
        self.hoursOfService = "Hours: Mo-Fr 10am-7pm"
        self.contactInstructions = "Call during business hours."
        self.roles = ["developer"]

    def validate(self):
        if self.identifier and not self.identifier:
            raise ValueError("identifier is a required field")
        # Add validation for other fields
        for link in self.links:
            link.validate()

class License:
    def __init__(self):
        self.licenseText = "MIT License"

    def validate(self):
        pass

class RecordGeoJSON:
    def __init__(self):
        self.id = "TBD"
        self.type = "Feature"
        self.time = Time()
        self.conformsTo = "http://www.opengis.net/spec/ogcapi-records-1/1.0/req/record-core"
        self.geometry = GeometryGeoJSON()

        current_timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        self.properties = {
            "type": "dataset",
            "title": "TBD",
            "description": "TBD",
            "created": current_timestamp,
            "updated": current_timestamp,
            "keywords": ["example"],
            "language": Language(),
            "resourceLanguages": [Language()],
            "themes": [Theme()],
            "formats": ["json", "html"],
            "contacts": [Contact()],
            "license": License(),
            "rights": "eMOTIONAL Cities 2021-2025 - All rights reserved."
        }
        self.links = [Link()]

    def validate(self):
        if not self.id:
            raise ValueError("id is a required field")
        if not self.id.startswith("http://") and not self.id.startswith("https://"):
            raise ValueError("Invalid id format")
        if self.type != "Feature":
            raise ValueError("type is a required field and should be 'Feature'")
        self.time.validate()
        self.geometry.validate()
        if not self.properties.get("type"):
            raise ValueError("properties.type is a required field")
        if not self.properties.get("title"):
            raise ValueError("properties.title is a required field")
        if self.properties.get("language"):
            self.properties["language"].validate()
        if self.properties.get("languages"):
            for lang in self.properties["languages"]:
                lang.validate()
        if self.properties.get("contacts"):
            for contact in self.properties["contacts"]:
                contact.validate()
        for link in self.links:
            link.validate()

    @classmethod
    def from_dict(cls, data: dict) -> "RecordGeoJSON":
        # Handle the properties fields directly within this method
        created = data.get('created')
        updated = data.get('updated')
        type_ = data['type']
        title = data['title']
        description = data.get('description')
        keywords = data.get('keywords', [])
        language = data.get('language')
        languages = data.get('languages', [])
        resourceLanguages = data.get('resourceLanguages', [])
        themes = [Theme.from_dict(item) for item in data.get('themes', [])]
        formats = data.get('formats', [])
        contacts = [Contact.from_dict(item) for item in data.get('contacts', [])]
        license_ = License.from_dict(data['license']) if data.get('license') else None
        rights = data.get('rights')
        links = [Link.from_dict(link) for link in data['links']]
        
        # Create the object and return
        return cls(
            id=data['id'],
            type_=type_,
            time=Time.from_dict(data['time']),
            geometry=GeometryGeoJSON.from_dict(data['geometry']) if data['geometry'] else None,
            created=created,
            updated=updated,
            title=title,
            description=description,
            keywords=keywords,
            language=language,
            languages=languages,
            resourceLanguages=resourceLanguages,
            themes=themes,
            formats=formats,
            contacts=contacts,
            license_=license_,
            rights=rights,
            links=links
        )


    def from_json_string(json_str):
        data = json.loads(json_str)
        return RecordGeoJSON.from_dict(data)

    def to_json(self):
        return json.dumps(self, indent=4, cls=ComplexEncoder)

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            return json.JSONEncoder.default(self, obj)

# record = RecordGeoJSON()
# print(record.to_json())
