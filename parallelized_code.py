import pandas as pd
from geopy.geocoders import Nominatim
from math import radians, sin, cos, sqrt, atan2

zip_codes = pd.read_csv('NC_Zip_Codes_Truncated.csv', header=None, names=['ZIP', 'Type', 'City', 'County', 'State', 'Area_Code'])
stations = pd.read_csv('NC_weather_annual2010_2021_V1.csv')

def get_lat_lon(zip_code):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(f"{zip_code} North Carolina")
    return (location.latitude, location.longitude) if location else (None, None)


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


unique_stations = stations.drop_duplicates(subset='STATION')[['STATION', 'LATITUDE', 'LONGITUDE']].set_index(
    'STATION').T.to_dict('list')

print("Starting distance calculations...")

distances = []
zips = []
zip_count = len(zip_codes)
for idx, row in zip_codes.iterrows():
    lat, lon = get_lat_lon(row['ZIP'])
    dist_for_zip = {}
    for station, coords in unique_stations.items():
        dist = haversine_distance(lat, lon, coords[0], coords[1])
        dist_for_zip[station] = dist
    distances.append(dist_for_zip)
    zips.append(row['ZIP'])

    if (idx + 1) % 10 == 0:
        print(f"Processed {idx + 1} out of {zip_count} ZIP codes.")

print("All distances calculated. Converting to DataFrame...")

distance_matrix = pd.DataFrame(distances, index=zips)

print("Process complete!")
print(distance_matrix)
distance_matrix.to_csv('zip_to_station_distances.csv', index_label='ZIP Code')