
import pandas as pd
import os
import matplotlib.pyplot as plt
import statistics

# read in the table with the wells in the Oligocene layers 
Wells = pd.read_excel(r'C:\PYTHON_CODE\Data\ListWells_Oligocene.xlsx')

# reading all the watertable height data 
Data=[]
for i in Wells.index.tolist():
    try:
        path = os.path.join(r'C:\PYTHON_CODE\Data', Wells.loc[i,'gw_id_Filter']+'.xlsx')
        name = pd.read_excel(path)
        Data.append(name)
    except:
        pass

#%% Filter wells with data in March, April,2019
SpatialTable2 = pd.DataFrame(columns=['Well', 'x', 'y', 'MeanGroundwaterLevel', 'LevelAutumn2018', 'Difference'])
StartAutumn2018 = pd.Timestamp(2018,9,1)
EndAutumn2018 = pd.Timestamp(2018,11,30)

for i in range(0,520):
    if Data[i].count()[0] > 1: # so that wells with only one measurement are not taken into account
        LevelsAutumn=[]      
        for k in Data[i].index.tolist():
            if StartAutumn2018 < Data[i].iloc[k,16] < EndAutumn2018:
                LevelsAutumn.append(Data[i].iloc[k,18])         
        try:
            LevelsAutumn2018 = statistics.mean(LevelsAutumn)
            SpTi = pd.DataFrame([Data[i].iloc[0,3],Data[i].iloc[0,6], Data[i].iloc[0,7],Data[i].mean()[-2],LevelsAutumn2018,LevelsAutumn2018 - Data[i].mean()[-2]], index=['Well', 'x', 'y', 'MeanGroundwaterLevel', 'LevelAutumn2018','Difference'])
            SpTi = SpTi.transpose()
            SpatialTable2 = SpatialTable2.append(SpTi)
        except:
            pass
        #%% MAP the diference between March-April 2019 and the average groundwater level.
import numpy as np
import pandas as pd
import glob
from pykrige.ok import OrdinaryKriging
from pykrige.kriging_tools import write_asc_grid
import pykrige.kriging_tools as kt
import matplotlib.pyplot as plt

from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Path, PathPatch

import geopandas as gdp

from mpl_toolkits.basemap import Basemap


df = SpatialTable2

lons = np.array(df['x']) 
lats = np.array(df['y']) 
data = np.array(df['Difference'])

plt.scatter(lons, lats, 15, data, cmap = plt.cm.Blues)
plt.xlabel("East")
plt.ylabel("North")
plt.title("data visualization")
cbar = plt.colorbar()
cbar.set_label("Data", labelpad=+1)
plt.show()

print("Variance: ", round(data.var(), 2))

OK = OrdinaryKriging(lons, lats, data, variogram_model='spherical', nlags=25, verbose=True, enable_plotting=True)
# z1, ss1 = OK.execute('grid', lons, lats)
# xintrp, yintrp = np.meshgrid(grid_lon, grid_lat)
# xintrp, yintrp = np.meshgrid(lons, lats)

grid_x = np.linspace(150000, 250000, num = 100, endpoint = False)
grid_y = np.linspace(160000, 220000, num = 100, endpoint = False)

z, ss = OK.execute('grid', grid_x, grid_y) # z are the data y ss the variance

kt.write_asc_grid(grid_x, grid_y, z, filename="kriging_ordinary.asc") #Ordinary Kriging in matrix form


kt.write_asc_grid(grid_x, grid_y, ss, filename="kriging_ordinary_var.asc") #Estimating variance in matrix form

asc = pd.read_csv("kriging_ordinary.asc", header=None, skiprows=7, sep="\s+") 
asc.shape #comprobar que sean 70 filas y 80 columnas

cu2 = np.array(asc) #Converting pandas dataframe to numpy array

#%%Plotting map with krigging interpolation
import geopandas as gdp
from descartes import PolygonPatch

gpo = gdp.read_file('C:/PYTHON_CODE/Data/Groundwaterbodies_Oligocene/Groundwaterbodies_Oligocene.shp')


fig = plt.figure(figsize = (12,12))
ax = fig.gca()

a = plt.imshow(cu2, cmap=plt.cm.YlOrBr, extent=[150000,250000,160000,220000]) #gist_rainbow
plt.grid(True)
cbar = fig.colorbar(a, orientation='horizontal', pad=0.05)
cbar.set_label("Values", labelpad=+1)
plt.xlabel('East')
plt.ylabel('North')
plt.title('Kriging Ordinary [no restriction]')
ax.scatter(lons, lats, c='blue')
for i in gpo['geometry']:
        ax.add_patch(PolygonPatch(i, fill=False, alpha=0.5, zorder=2, hatch='////'))
plt.show()
#Save as PDF document
fig.savefig("foo.pdf", bbox_inches='tight')
