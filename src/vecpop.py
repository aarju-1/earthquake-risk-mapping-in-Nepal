

import geopandas as gpd
from rasterstats import zonal_stats
import os


def calculate_population_by_district(shapefile_path, raster_path, output_path):
    """
    Calculate population per district using zonal statistics.

    Parameters
    ----------
    shapefile_path : str
        Path to the district shapefile.
    raster_path : str
        Path to the population raster (.tif).
    output_path : str
        Path to save the output GeoJSON and Shapefile.
    """
    # 1. Load district boundaries
    districts = gpd.read_file(shapefile_path)

    # 2. Run zonal statistics (sum of population in each district)
    stats = zonal_stats(
        districts,
        raster_path,
        stats="sum",
        geojson_out=True
    )

    # 3. Convert results back to GeoDataFrame
    district_pop = gpd.GeoDataFrame.from_features(stats)
    district_pop = district_pop.set_crs(districts.crs)  # ensure CRS matches

    # 4. Rename population column
    district_pop = district_pop.rename(columns={"sum": "population"})

    # 5. Save results
    geojson_file = os.path.join(output_path, "district_population.geojson")
    shp_file = os.path.join(output_path, "district_population.shp")

    district_pop.to_file(geojson_file, driver="GeoJSON")
    district_pop.to_file(shp_file, driver="ESRI Shapefile")

  
    print(district_pop[["DISTRICT", "population"]].head())

    return district_pop


if __name__ == "__main__":
    # Input paths (modify according to your project structure)
    shapefile = r"D:\Projects\GIS\earthquake-risk-mapping-in-Nepal\data\Nepal Districts Shapefile Download\03_DISTRICT\DISTRICT.shp"
    raster = r"D:\Projects\GIS\earthquake-risk-mapping-in-Nepal\data\npl_pop_2025_CN_100m_R2025A_v1.tif"
    output_dir = r"D:\Projects\GIS\earthquake-risk-mapping-in-Nepal\output"

    os.makedirs(output_dir, exist_ok=True)

    # Run calculation
    calculate_population_by_district(shapefile, raster, output_dir)