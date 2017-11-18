import geopandas as gpd
import autoargs

@autoargs
def main(input_file: gpd.GeoDataFrame):
	input_file.to_crs(...)
	return input_file
