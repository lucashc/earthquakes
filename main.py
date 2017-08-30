import pandas as pd
import numpy as np
import netCDF4
from folium import plugins
import folium
import base64
import datetime
import matplotlib.pyplot as plt

ds = netCDF4.Dataset('data.nc', 'r', format="NETCDF4")
W = np.array(ds.variables['magnitude']) / 6
X = np.array(ds.variables['lat'])
Y = np.array(ds.variables['lon'])
Z = np.array(ds.variables['time'])

data = pd.DataFrame(data=np.vstack([X, Y, W]).T, columns=['lat', 'lon', 'weight'])
times = pd.DataFrame(data=pd.to_datetime(Z.T, unit='s', origin=pd.Timestamp('1900-01-01')), columns=['time'])

data = pd.concat([data, times], axis=1).sort_values(by='time')

# Split in 10 equal pieces

# Split every 10 years, first earthquak recorded is 1911-05-30
# Start at 1901-01-01


mp = folium.Map(location=[51.5, 4], zoom_start=7)

hm = plugins.HeatMap(data.as_matrix(columns=['lat', 'lon', 'weight']).tolist())

hm.add_to(mp)

plt.scatter(data.as_matrix(columns=['time']).T, data.as_matrix(columns=['weight']).T * 6)
plt.title("Spread of earthquakes")
plt.xlabel("Time in years")
plt.ylabel("Intensity Richters scale")
plt.ylim(ymin=0)
plt.savefig('scatter.png')

# convert to base64

imo = plugins.FloatImage('data:image/png;base64,' + base64.b64encode(open('scatter.png', 'rb').read()).decode('utf-8'), bottom=5, left=1)

imo.add_to(mp)

mp.save('test.html')
