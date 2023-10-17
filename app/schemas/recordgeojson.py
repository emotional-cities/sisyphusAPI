from typing import List, Union, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl, constr
from datetime import datetime
import json

DatePattern = constr(regex="^\\d{4}-\\d{2}-\\d{2}$")
TimestampPattern = constr(regex="^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d+)?Z$")
IntervalItemPattern = Union[DatePattern, TimestampPattern, str]  # Note: Added "str" for ".."

class Time(BaseModel):
    date: Optional[DatePattern]
    timestamp: Optional[TimestampPattern]
    interval: Optional[List[IntervalItemPattern]]
    resolution: Optional[str]  # Since no constraints were mentioned other than an example.

    def to_json(self) -> str:
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, json_str: str) -> "Time":
        return cls(**json.loads(json_str))

class Point(BaseModel):
    type: str = 'Point'
    coordinates: List[float]

    def to_json(self) -> str:
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, json_str: str) -> "Point":
        return cls(**json.loads(json_str))

class MultiPoint(BaseModel):
    type: str = 'MultiPoint'
    coordinates: List[List[float]]

    def to_json(self) -> str:
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, json_str: str) -> "MultiPoint":
        return cls(**json.loads(json_str))

class LineString(BaseModel):
    type: str = 'LineString'
    coordinates: List[List[float]]

    def to_json(self) -> str:
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, json_str: str) -> "LineString":
        return cls(**json.loads(json_str))

class MultiLineString(BaseModel):
    type: str = 'MultiLineString'
    coordinates: List[List[List[float]]]

    def to_json(self) -> str:
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, json_str: str) -> "MultiLineString":
        return cls(**json.loads(json_str))

class Polygon(BaseModel):
    type: str = 'Polygon'
    coordinates: List[List[List[float]]]

    def to_json(self) -> str:
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, json_str: str) -> "Polygon":
        return cls(**json.loads(json_str))

class MultiPolygon(BaseModel):
    type: str = 'MultiPolygon'
    coordinates: List[List[List[List[float]]]]

    def to_json(self) -> str:
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, json_str: str) -> "MultiPolygon":
        return cls(**json.loads(json_str))

class GeometryCollection(BaseModel):
    type: str = 'GeometryCollection'
    geometries: List[
        Union[
            Point,
            MultiPoint,
            LineString,
            MultiLineString,
            Polygon,
            MultiPolygon
        ]
    ]

    def to_json(self) -> str:
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, json_str: str) -> "GeometryCollection":
        data = json.loads(json_str)
        geometry_type = data.get("type").lower()

        if geometry_type != "GeometryCollection":
            raise ValueError(f"Expected GeometryCollection type but got: {geometry_type}")

        geometry_model_map = {
            "point": Point,
            "multipoint": MultiPoint,
            "linestring": LineString,
            "multilinestring": MultiLineString,
            "polygon": Polygon,
            "multipolygon": MultiPolygon,
            "geometrycollection": GeometryCollection
        }

        # Convert each geometry in the 'geometries' list to the appropriate model
        converted_geometries = []
        for geometry_data in data["geometries"]:
            geom_type = geometry_data["type"]
            if geom_type not in geometry_model_map:
                raise ValueError(f"Unsupported geometry type: {geom_type}")
            converted_geometries.append(geometry_model_map[geom_type](**geometry_data))

        return cls(type=geometry_type, geometries=converted_geometries)

class Language(BaseModel):
    code: str
    name: Optional[constr(min_length=1)]
    alternate: Optional[str]
    dir: str = "ltr"  # Default set to "ltr"

    def to_json(self) -> str:
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, json_str: str) -> "Language":
        return cls(**json.loads(json_str))

class Concept(BaseModel):
    id: str
    title: Optional[str]
    description: Optional[str]
    url: Optional[HttpUrl]

class Theme(BaseModel):
    concepts: List[Concept]
    scheme: str

    def to_json(self) -> str:
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, json_str: str) -> "Theme":
        return cls(**json.loads(json_str))

class Link(BaseModel):
    href: HttpUrl
    rel: Optional[str]
    type: Optional[str]
    hreflang: Optional[str]
    title: Optional[str]
    templated: Optional[bool]
    variables: Optional[Dict[str, Any]]
    created: Optional[datetime]
    updated: Optional[datetime]

    def to_json(self) -> str:
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, json_str: str) -> "Link":
        return cls(**json.loads(json_str))

class Roles(BaseModel):
    roles: List[str]

    def to_json(self) -> str:
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, json_str: str) -> "Roles":
        return cls(**json.loads(json_str))

class PhoneNumber(BaseModel):
    value: constr(regex="^\\+[1-9]{1}[0-9]{3,14}$")
    roles: Optional[Roles]

class Email(BaseModel):
    value: str
    roles: Optional[Roles]

class Address(BaseModel):
    deliveryPoint: Optional[List[str]]
    city: Optional[str]
    administrativeArea: Optional[str]
    postalCode: Optional[str]
    country: Optional[str]
    roles: Optional[Roles]

class Contact(BaseModel):
    identifier: Optional[str]
    name: Optional[str]
    position: Optional[str]
    organization: Optional[str]
    logo: Optional[Link]
    phones: Optional[List[PhoneNumber]]
    emails: Optional[List[Email]]
    addresses: Optional[List[Address]]
    links: Optional[List[Link]]
    hoursOfService: Optional[str]
    contactInstructions: Optional[str]
    roles: Optional[Roles]

    def to_json(self) -> str:
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, json_str: str) -> "Contact":
        return cls(**json.loads(json_str))

class ExternalId(BaseModel):
    scheme: Optional[str]
    value: str

class Properties(BaseModel):
    created: Optional[datetime]
    updated: Optional[datetime]
    type: constr(max_length=64)
    title: str
    description: Optional[str]
    keywords: Optional[List[str]]
    language: Optional[Language]
    languages: Optional[List[Language]]
    resourceLanguages: Optional[List[Language]]
    externalIds: Optional[List[ExternalId]]
    themes: List[Theme]
    formats: Optional[List[str]]
    contacts: Optional[List[Contact]]
    license: Optional[constr(regex="^(.+|other)$")]
    rights: Optional[str]


class RecordGeoJSON(BaseModel):
    id: str
    type: str
    conformsTo: Optional[List[str]]
    time: Time
    geometry: Union[
        Point,
        MultiPoint,
        LineString,
        MultiLineString,
        Polygon,
        MultiPolygon,
        GeometryCollection,
        None
    ]
    properties: Properties
    links: List[Link]

    def to_json(self) -> str:
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, json_str: str) -> "RecordGeoJSON":
        return cls(**json.loads(json_str))


# record = RecordGeoJSON.from_json(some_json_str)
# record_json = record.to_json()
