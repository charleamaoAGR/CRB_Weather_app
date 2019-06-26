from netCDF4 import Dataset

dataset = Dataset('Timi_data.nc', 'w', format='NETCDF4_CLASSIC')

level = dataset.createDimension('level', 10)
lat = dataset.createDimension('lat', 49)
lon = dataset.createDimension('lon', 100)
time = dataset.createDimension('time', None)

print dataset