# работа скрипта не гарантируется
# уточните вызовы функций в документации pandas/geopandas

from utils import autoargs
import geopandas as gpd


@autoargs
def attribute(objects: gpd.GeoDataFrame, regions: gpd.GeoDataFrame):
	# пересечение
	intersection = gpd.sjoin(regions, objects, how='inner', op='intersects')
	# приклеиваем обратно пару
	merged = objects.merge(intersection[['index_right', 'region_id']], left_on='index_right', right_on='index_left')
	return gpd.GeoDataFrame(merged, crs=objects.crs)
