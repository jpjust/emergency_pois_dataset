from cityzones import osmpois, overpass
from os import listdir
from os.path import isfile, join
import json
import requests

files = [f for f in listdir('../geojson') if isfile(join('../geojson', f))]
files.sort()
csv_fp = open('../csv/dataset.csv', 'w')
csv_fp.write('City;Hospitals;Fire stations;Police stations;Railway stations;Total PoIs;Types of PoIs\n')

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
    geojson_fp = open(f'../geojson/{file}', 'r')
    geojson = json.load(geojson_fp)
    geojson_fp.close()

    city = geojson['name']
    print(city)
    osm_file = f'../osm/{city}.osm'

    if not isfile(osm_file):
        poly_list = []
        polygons = geojson['features'][0]['geometry']['coordinates']
        for polygon in polygons:
            poly_list += polygon[0]

        while True:
            try:
                osm_xml = overpass.get_osm_from_polygon(poly_list, 600)
                break
            except requests.exceptions.ConnectionError:
                print('Connection error. Trying again...')
            except requests.exceptions.ReadTimeout:
                print('Connection time-out. Trying again...')

        osm_fp = open(osm_file, 'w')
        osm_fp.write(osm_xml)
        osm_fp.close()

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
    
    total_pois = hospitals + fire_stations + police_stations + railway_stations
    types_pois = (hospitals > 0) + (fire_stations > 0) + (police_stations > 0) + (railway_stations > 0)

    csv_fp.write(f'{city};{hospitals};{fire_stations};{police_stations};{railway_stations};{total_pois};{types_pois}\n')

    geojson['features'][0]['properties']['hospitals'] = hospitals
    geojson['features'][0]['properties']['fire_stations'] = fire_stations
    geojson['features'][0]['properties']['police_stations'] = police_stations
    geojson['features'][0]['properties']['railway_stations'] = railway_stations
    geojson['features'][0]['properties']['total_pois'] = total_pois
    geojson['features'][0]['properties']['types_of_pois'] = types_pois
    
    geojson_fp = open(f'../geojson/{file}', 'w')
    json.dump(geojson, geojson_fp)
    geojson_fp.close()

csv_fp.close()
