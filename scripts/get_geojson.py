from os.path import isfile
import json

FILEPATH = '../source_geojson/portugal_full.geojson'

fp = open(FILEPATH, 'r')
geojson = json.load(fp)
fp.close()

for feature in geojson['features']:
    city = feature['properties']['Concelho']
    geojson_file = f'../geojson/{city}.geojson'
    if isfile(geojson_file):
        continue

    coordinates = feature['geometry']

    fp = open(geojson_file, 'w')
    output = {
        "type": "FeatureCollection",
        "name": city,
        "crs": {
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
            }
        },
        "features": [{
            "type": "Feature",
            "properties": {
                "NAME_1": city
            },
            "geometry": coordinates
        }]
    }
    print(city)
    json.dump(output, fp)
    fp.close()
