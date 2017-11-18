# работа скрипта не гарантируется
# уточните вызовы функций в документации pandas/geopandas

from utils import autoargs
import geopandas as gpd

@autoargs
def group(objects: gpd.GeoDataFrame, regions: gpd.GeoDataFrame):
	intersection = gpd.sjoin(regions, objects, how='inner', op='intersects')
	grouped = intersection.groupby(by='index_right').agg({'population': 'sum', 'beer_shops': 'count', 'name': 'first'}).reset_index()

	# добавляю обратно
	result = regions.merge(grouped, left_index=True, right_on='index_right')
	return gpd.GeoDataFrame(result, crs=objects.crs)
