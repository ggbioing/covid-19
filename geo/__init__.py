"""
Requirements: geopandas, pandas

Requirements for plotting

	contextly (to add background)
		conda install -c conda-forge cartopy
		conda install -c conda-forge proj
		conda install folium -c conda-forge
		conda install -c conda-forge mapclassify  # for quantile plot etc.
"""
from pathlib import Path
import geopandas as gpd
import pandas as pd
# import folium

MAP_DIR = Path(__file__).parent / 'map'

ter_dict = {  # dictionary of territories for compatibility between Istat csv and geojson files
	'provincia autonoma bolzano / bozen': 'bolzano/bozen',
	'provincia autonoma trento': 'trento',
	"valle d'aosta / vallée d'aoste": "valle d'aosta/vallée d'aoste",
	# REGIONI
	'trentino-alto adige / südtirol': 'trentino-alto adige/südtirol',
}


class Mapper():

	def __init__(self, mapper, invert=False):
		self.mapper = mapper
		self.invert = invert

	def __call__(self, s):
		mapper_ = {v: k for k, v in self.mapper.items()} if self.invert else self.mapper
		try:
			return mapper_[s]
		except KeyError:
			return s


COM = gpd.read_file(MAP_DIR / 'it/comuni.geojson').rename(str.lower, axis=1)

PROV = gpd.read_file(MAP_DIR / 'it/province.geojson')
PROV['prov_name'] = PROV['prov_name'].str.lower().map(Mapper(ter_dict, invert=True))
PROV['reg_name'] = PROV['reg_name'].str.lower().map(Mapper(ter_dict, invert=True))

REG = PROV[['reg_name', 'geometry']].dissolve('reg_name').reset_index()

"""ISTAT"""
DEMOG = pd.read_csv(MAP_DIR / '../../istat/demog.csv').rename(mapper={'Territorio': 'prov_name', 'Value': 'population'}, axis=1)
tmp = DEMOG['prov_name'].str.lower()
DEMOG['prov_name'] = tmp
del tmp


# # # Trova nome comune a partire da coordinate gps
def find_place(coords):
	reg_name = REG[REG.contains(coords)]['reg_name'].iloc[0]
	prov = PROV.query(f'reg_name=="{reg_name}"')
	prov_name = prov[prov.contains(coords)]['prov_name'].iloc[0]
	del prov
	com_name = COM[COM.contains(coords)]['nome_com'].iloc[0]
	print(com_name, prov_name, reg_name)
	return com_name, prov_name, reg_name


# def plot_gdf_folium(gdf):
# 	bo = gdf.total_bounds
# 	center = (bo[1] + bo[3])/2, (bo[0] + bo[2])/2
# 	m = folium.Map(center, zoom_start=10, tiles='OpenStreetMap')
# 	folium.GeoJson(gdf).add_to(m)
# 	return m


__all__ = [
	'COM',
	'PROV',
	'REG',
	'find_place',
	# 'plot_gdf_folium',
]