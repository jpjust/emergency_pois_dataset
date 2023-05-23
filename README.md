# Emergency PoIs dataset

This repository contains a dataset of GeoJSON and OSM data from Portuguese cities that were used to computed the number of emergency PoIs in each city.

The file in `source_geojson` folder was used to extract a GeoJSON for each city. The full GeoJSON of Portugal was extracted from a Shapefile of the whole country.

The files in `geojson` folder contains GeoJSON data for each city. Then, OpenStreetMap data was retrived via [Overpass API](https://dev.overpass-api.de/overpass-doc/en/index.html) to provide a set of OSM files for each city, stored in `osm` folder.

A CSV file with the number of hospitals, fire stations, police stations and railway stations is present in `csv` folder.

Finally, the scripts used to generate the files are inside the `scripts` folder. You will need [CityZones](https://cityzones.just.pro.br).
