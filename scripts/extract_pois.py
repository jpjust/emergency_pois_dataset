from cityzones import osmpois, overpass
from os import listdir
from os.path import isfile, join
import json

files = [f for f in listdir('../geojson') if isfile(join('../', f))]
files.sort()

csv_fp = open('../csv/dataset.csv', 'w')
csv_fp.write('City;Hospitals;Fire stations;Police stations;Railway stations\n')

pois_type = {
    "amenity": {
        "fire_station": {
            "w": 5.0
        },
        "hospital": {
            "w": 10.0
        },
        "police": {
            "w": 2.0
        }
    },
    "railway": {
        "station": {
            "w": 1.0
        }
    }
}

for file in files:
    fp = open(f'../geojson/{file}', 'r')
    geojson = json.load(fp)
    fp.close()

    poly_list = []
    polygons = geojson['features'][0]['geometry']['coordinates']
    for polygon in polygons:
        poly_list += polygon[0]

    city = geojson['name']
    print(city)
    osm_file = f'../osm/{city}.osm'
    if not isfile(osm_file):
        osm_xml = overpass.get_osm_from_polygon(poly_list, 600)
        fp = open(osm_file, 'w')
        fp.write(osm_xml)
        fp.close()

    pois, roads = osmpois.extract_pois(osm_file, pois_type)
    hospitals = fire_stations = police_stations = railway_stations = 0
    for poi in pois:
        if 'railway' in poi.keys():
            railway_stations += 1
        elif 'amenity' in poi.keys():
            if poi['amenity'] == 'hospital':
                hospitals += 1
            elif poi['amenity'] == 'fire_station':
                fire_stations += 1
            elif poi['amenity'] == 'police':
                police_stations += 1
    
    csv_fp.write(f'{city};{hospitals};{fire_stations};{police_stations};{railway_stations}\n')

csv_fp.close()
