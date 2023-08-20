# Sisyphus API

TODO...

## Requirements


## Running with Docker
To run the API with Docker, you can follow these steps:

1. Clone the repository

```bash
git clone git@TODO
```

2. Build the Docker image using the following command:

```bash
docker build . -t sisyphus-api --no-cache
```

3. Start the Docker container with the following command:

```bash
docker run -p 80:80 sisyphus-api
```

However, to make the API functional, you need to provide environment variables that point to the required services. Specifically, you need to set the following environment variables:

- ENV_STATE: Set to `dev`


These variables can be set using the -e flag when running the Docker container. For example:

```bash
docker run -p 80:80 \
-e ENV_STATE=dev \
sisyphus-api
```

## Running Locally

To run the API locally, you can follow these steps:

Create an .env file, in the root of the project, with following example content:

```bash
ENV_STATE="dev"
DEV_LOG_PATH="./logs"
DEV_LOG_FILENAME="sisyphus.log"
DEV_LOG_LEVEL="DEBUG"
DEV_LOG_ROTATION="500 MB"
DEV_LOG_RETENTION="10 days"
DEV_LOG_FORMAT="{time} {level} {message}"
```

From the project folder, activate the [Poetry](https://python-poetry.org/) environment and start the API using the following command:

```bash
poetry shell
poetry run uvicorn app.main:app --host 0.0.0.0 --port 5000
```

The Swagger interface will be available at:

`http://localhost:5000/sisyphus/api/v1/docs`


## Building and Pushing the Docker Image

To build and push the Docker image, you can follow these steps:

1. Build the Docker image using the following command:

```bash
docker build . -t <your-docker-username>/sisyphus-api --no-cache
```

2. Push the Docker image to Docker Hub using the following command:

```bash
docker push <your-docker-username>/sisyphus-api
```

Note that you need to replace `<your-docker-username>` with your Docker Hub username.

Note that default port used by docker container will be `80` instead of `5000`.

## Environment Variables

|Variable Name                    |Description                         |
|---------------------------------|------------------------------------|
|ENV_STATE                        |Environment state (e.g., dev, prod) |

## API Endpoints

The [Swagger](https://swagger.io/) documentation is available at the following endpoint:

`/sisyphus/api/v1/docs`

## Loading sample data

You can load sample data from ./data/sample_data.json, you can use elasticdump 

To install elasticdump you need npm

```bash
npm install elasticdump
```

To load data you can run:

```bash
elasticdump --input=./data/sample_data.json --output=http://localhost:9200
```

To test that the sample data is loaded:

```bash
curl -X GET "localhost:9200/ec_catalog/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "id": "pp_tobacco"
    }
  }
}
'
```
It should output something like 

```json
{
  "took" : 5,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 4.2314334,
    "hits" : [
      {
        "_index" : "ec_catalog",
        "_id" : "pp_tobacco",
        "_score" : 4.2314334,
        "_source" : {
          "recordUpdated" : "2023-08-10T10:56:07.525921623Z",
          "type" : "Feature",
          "conformsTo" : "http://www.opengis.net/spec/ogcapi-records-1/1.0/req/record-core",
          "geometry" : {
            "coordinates" : [
              [
                [
                  -9.229835564339478,
                  38.69139933303907
                ],
                [
                  -9.08738707964508,
                  38.69139933303907
                ],
                [
                  -9.08738707964508,
                  38.79675969109248
                ],
                [
                  -9.229835564339478,
                  38.79675969109248
                ],
                [
                  -9.229835564339478,
                  38.69139933303907
                ]
              ]
            ],
            "type" : "Polygon"
          },
          "properties" : {
            "language" : "en",
            "keywords" : [
              "urban health, health, life style, IGOT, Lisbon"
            ],
            "formats" : [
              "HTML",
              "GeoJSON"
            ],
            "links" : [
              "https://emotional.byteroad.net/collections/pp_tobacco",
              "https://emotional.byteroad.net/collections/pp_tobacco/tiles",
              "https://emotional.byteroad.net/geoserver/ows?service=WMS&version=1.3.0&request=GetCapabilities"
            ],
            "contacts" : {
              "emails" : {
                "value" : " info@igot.ul.pt"
              },
              "organization" : "IGOT",
              "name" : "Name Lastname"
            },
            "type" : "dataset",
            "updated" : "2023-08-10T10:56:07.525921623Z",
            "created" : "2023-08-10T10:56:07.525921623Z",
            "title" : "Patients with tobacco abuse",
            "description" : "Data Platform IGOT - Urban health",
            "themes" : {
              "concepts" : [
                "Urban Health Data"
              ]
            },
            "license" : "Creative Commons (CC BY 4.0)"
          },
          "@version" : "1",
          "@timestamp" : "2023-08-10T10:56:07.525921623Z",
          "recordCreated" : "2023-08-10T10:56:07.525921623Z",
          "time" : {
            "resolution" : "P1D",
            "interval" : 2021
          },
          "id" : "pp_tobacco"
        }
      }
    ]
  }
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
