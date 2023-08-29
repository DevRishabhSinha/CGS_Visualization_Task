import pandas as pd

zip_to_station_df = pd.read_csv('zip_to_station_distances.csv')
hdd_df = pd.read_csv('Weather_Station_HDD.csv')

hdd_df.dropna(subset=['HTDD'], inplace=True)
hdd_df['HTDD'] = pd.to_numeric(hdd_df['HTDD'])

results = []

for _, zip_row in zip_to_station_df.iterrows():
    zip_code = zip_row['ZIP Code']

    for year in hdd_df['year'].unique():
        year_df = hdd_df[hdd_df['year'] == year]

        total_weighted_hdd = 0
        total_weight = 0
        for station, hdd_row in year_df.iterrows():
            station_id = hdd_row['STATION']
            if station_id in zip_row:
                distance = zip_row[station_id]
                if distance != 0:
                    weight = 1 / distance
                    total_weighted_hdd += hdd_row['HTDD'] * weight
                    total_weight += weight

        if total_weight != 0:
            weighted_avg = total_weighted_hdd / total_weight
        else:
            weighted_avg = None

        results.append({'ZIP Code': zip_code, 'year': year, 'Weighted Average HDD': weighted_avg})

results_df = pd.DataFrame(results)
print(results_df)

results_df.to_csv('output.csv', index=False)
