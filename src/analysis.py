# analysis code will go here
import geopandas as gpd
import pandas as pd
import json
from datetime import datetime,timedelta

def process_earthquake_data(json_path, output_excel=None):
    """
    Process USGS earthquake JSON data and convert it to a clean DataFrame.
    
    Parameters:
    - json_path: str, path to the USGS JSON file.
    - output_excel: str or None, path to save the Excel file. If None, no file is saved.
    
    Returns:
    - pd.DataFrame with columns: magnitude, place, time, longitude, latitude, depth
    """
    # Load JSON data
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    earthquakes_cleaned = []

    for feature in data['features']:
        eq = feature['properties']
        coords = feature['geometry']['coordinates']
        
        # Convert timestamp (handles pre-1970 times)
        try:
            ts_ms = eq['time']
            ts_sec = ts_ms / 1000
            readable_time = datetime(1970, 1, 1) + timedelta(seconds=ts_sec)
            readable_time = readable_time.strftime('%Y-%m-%d %H:%M:%S')
        except (OSError, OverflowError, TypeError, KeyError):
            readable_time = None
        
        earthquakes_cleaned.append({
            'magnitude': eq.get('mag'),
            'place': eq.get('place'),
            'time': readable_time,
            'longitude': coords[0],
            'latitude': coords[1],
            'depth': coords[2]
        })

    # Convert to DataFrame
    df = pd.DataFrame(earthquakes_cleaned)

    # Save to Excel if path provided
    if output_excel:
        df.to_excel(output_excel, index=False)
    
    return df

df_eq = process_earthquake_data(
    json_path=r"D:\Projects\GIS\earthquake-risk-mapping-in-Nepal\data\query.json",
    output_excel=r"D:\Projects\GIS\earthquake-risk-mapping-in-Nepal\data\earthquakes.xlsx")
