
def read_file(fname, crs=None, driver=None):
	if fname is None:
		return

	if fname.startswith('postgresql://'):
		engine, table_or_query = _connect_postgres(fname)
		df = pd.read_sql(table_or_query, engine)

		print('Exported from Postgres.')
		if 'geometry' in df:
			df['geometry'] = df['geometry'].apply(bytes.fromhex).apply(wkb.loads)
			return gpd.GeoDataFrame(df)

		return df

	elif fname.endswith('.geojson') or driver == 'GeoJSON':
		source_df = gpd.read_file(fname, driver='GeoJSON')
		if crs:
			source_df.crs = crs

	elif fname.endswith('.json'):
		source_df = pd.read_json(fname)

	elif fname.endswith('.csv') or driver == 'CSV':
		source_df = pd.read_csv(fname)
		if 'geometry' in source_df:
			try:
				source_df['geometry'] = source_df.geometry.apply(lambda g: wkt.loads(g))
			except AttributeError:
				print("warning: can't transform empty or broken geometry")
			else:
				source_df = gpd.GeoDataFrame(source_df)
		if crs:
			source_df.crs = crs

	elif '.gpkg' in fname:
		layername = None
		if '.gpkg:' in fname:
			try:
				fname, layername = fname.split(':')
			except ValueError as e:
				raise argh.CommandError('File name should be name.gpkg or name.gpkg:layer_name. Got "%s" instead.' % fname)
		else:
			layername = os.path.splitext(os.path.basename(fname))[0]

		source_df = gpd.read_file(fname, driver='GPKG', layer=layername)
		if crs:
			source_df.crs = crs

	return source_df

def write_file(df, fname):
	if fname.startswith('postgresql://'):
		engine, table_name = _connect_postgres(fname)
		df = df[list(df)]
		if 'geometry' in df:
			df['geometry'] = df['geometry'].apply(wkb.dumps).apply(bytes.hex)

		with engine.begin() as connection:
			pd.io.sql.execute('DROP TABLE IF EXISTS %s' % table_name, connection)
			df.to_sql(table_name, connection, chunksize=1000)
			pd.io.sql.execute("""
				ALTER TABLE %s
				ALTER COLUMN "geometry" TYPE Geometry""" % table_name, connection)

	elif isinstance(df, gpd.GeoDataFrame):
		df = df[df.geometry.notnull()]
		types = set(df.geometry.apply(lambda g: g.type).values)
		if len(types) > 1:  # trying to fix by making multipart geometries
			from . import utils
			df['geometry'] = df['geometry'].apply(utils.single_to_multi)

		if os.path.exists(fname):
			os.unlink(fname)
		if fname.endswith('.csv'):
			df = pd.DataFrame(df)
			df.to_csv(fname, index=False)
		elif fname.endswith('.gpkg'):
			df.to_file(fname, driver='GPKG', encoding='utf-8')
		else:
			df.to_file(fname, driver='GeoJSON', encoding='utf-8')

	elif isinstance(df, pd.DataFrame):
		if fname.endswith('.json'):
			df.to_json(fname)
		else:
			df.to_csv(fname)


@decorator
def _autoargs(func, *args, **kwargs):
	execution_start = time.time()

	func_signature = signature(func)
	newargs = [a for a in args]

	writer = None
	for i, (value, param) in enumerate(zip(args, func_signature.parameters.values())):
		if (
			param.annotation == AnyDataFrame or
			(param.annotation == gpd.GeoDataFrame and (value.endswith('.csv') or value.endswith('.geojson') or value.endswith('.gpkg'))) or
			param.annotation == pd.DataFrame
		):
			value = read_file(value)
		elif param.name in ('outfile', 'output_file'):
			# сохранить outfile_name в отдельную переменную, потому что value меняется
			outfile_name = value
			def writer(df):
				write_file(df, outfile_name)
		elif param.annotation == int and value:
			value = int(value)
		elif param.annotation == float and value:
			value = float(value)

		newargs[i] = value

	retval = func(*newargs, **kwargs)
	if writer and retval is not None:
		writer(retval)

	print('Full execution time {0}s'.format(timedelta(seconds=time.time()-execution_start)))


def autoargs(func):
	import inspect
	frm = inspect.stack()[1]
	mod = inspect.getmodule(frm[0])
	func2 = _autoargs(func)
	if mod.__name__ == '__main__':
		argh.dispatch_command(func2)
	else:
		# если команда не дефолтная, то надо сделать ручку для неё, чтобы вызывать из шелл-скриптов через setup.py
		def fn2():
			argh.dispatch_command(func2)

		mod._argh = fn2

	return func
