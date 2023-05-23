import json

FILEPATH = '../source_geojson/portugal_full.geojson'

fp = open(FILEPATH, 'r')
geojson = json.load(fp)
fp.close()

for feature in geojson['features']:
    city = feature['properties']['NAME_2']
    coordinates = feature['geometry']

    fp = open(f'{city}.geojson', 'w')
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
    json.dump(output, fp)
    fp.close()
