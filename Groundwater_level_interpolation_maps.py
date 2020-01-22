import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np 
import statistics

# set the working directory to the map with the data
os.chdir('C:\\Users\\Julio\\Desktop\\IUPWARE\\ENVIRONMENTAL PROGRAMMING\\Project Groundwater\\Data')
Dir=os.getcwd() #method returning the current working directory

#reading data
#ListWells_Oligocene.xlsx
def Read_Data(file):
    # read in the table with the wells in the Oligocene layers 
    Wells=pd.read_excel(file)

    # reading all the watertable height data 
    Data=[]
    for i in Wells.index.tolist():
        try:
            path=str(Dir+'\\'+Wells.loc[i,'gw_id_Filter']+'.xlsx')
            name=pd.read_excel(path)
            Data.append(name)
        except:
            pass
    return (Data)

#Plot of the evolution of water tables
#Ex1

def Fig_Evolution_WaterLevel(Data):
    """This function will first normalize the water levels for each monitoring well in
    the file that is choosen to be read by the user. These water levels are normalized by
    subtracting the mean water level of a certain monitoring well from each measurement of this well.
    The calculated normalized data are then visualized on a graph by dots in different colors.
    Every dot with the same color belongs to the same monitoring well. Also the mean water level is 
    visualized by a red line"""

    FigEvolution=plt.figure(figsize=(9,6))
    plt.xlabel('Year')
    plt.grid(axis='y')
    plt.ylabel('Deviation from mean')
    plt.title('Oligocene (Normalized Data)')  
    Data_Mean=np.zeros(len(Data)-1) 
    for j in range (0,len(Data)-1):
        Data_Mean[j]=np.mean(Data[j].iloc[:,18])
        plt.plot(Data[j].iloc[:,16], Data[j].iloc[:,18]-Data_Mean[j],".", Data[j].iloc[:,16], Data[j].iloc[:,18]-Data[j].iloc[:,18],'r') #Data_Mean sometimes has "nan" because no measurement has been done for that filter or monitoring well.
    return(FigEvolution)
    
#Fig_Evolution_WaterLevel(Data) 
      
#Ex2        

def GW_body_group(List_of_Wells, GW_body_code, Data):
    """This function takes as argument the file which contains the list of the wells (List_of_Wells), 
    the groundwater body code (GW_body_code), and the data of the wells (Data). This function goes 
    over the list of the wells to check which wells belong to that groundwater body. If so, the 
    data of the well is appended to the data of the groundwater body. The groundwater body data 
    is the output of the function."""

    Data_GW_body=[]
    for i in range(len(List_of_Wells)): #.index.tolist():   
        Data_GWL_C = List_of_Wells.loc[i][7] # 12 was initially 'groundwater body_code', but it didn't work either.
        if Data_GWL_C == GW_body_code: #Data_GWL_C = Data groundwatervody_code
            Data_GW_body.append(Data[i])
    return Data_GW_body    
    
#Plotting the normalized data for each groundwater body from 2010-2020
#Data_BLKS_0400_GWL_1S = GW_body_group(Wells, 'BLKS_0400_GWL_1S')        
#Fig_Evolution_WaterLevel(Data_BLKS_0400_GWL_1S)
#plt.title('Normalized Data: BLKS_0400_GWL_1S')
#plt.xlim(pd.Timestamp(2010,1,1),pd.Timestamp(2020,1,1)) #The assignment says to plot the period 2010-now
#
#Data_BLKS_0400_GWL_2S = GW_body_group(Wells, 'BLKS_0400_GWL_2S')        
#Fig_Evolution_WaterLevel(Data_BLKS_0400_GWL_2S)
#plt.title('Normalized Data: BLKS_0400_GWL_2S')
#plt.xlim(pd.Timestamp(2010,1,1),pd.Timestamp(2020,1,1))
#
#Data_BLKS_0400_GWL_1M = GW_body_group(Wells, 'BLKS_0400_GWL_1M')        
#Fig_Evolution_WaterLevel(Data_BLKS_0400_GWL_1M)
#plt.title('Normalized Data: BLKS_0400_GWL_1M')
#plt.xlim(pd.Timestamp(2010,1,1),pd.Timestamp(2020,1,1))
#
#Data_BLKS_0400_GWL_2M = GW_body_group(Wells, 'BLKS_0400_GWL_2M')        
#Fig_Evolution_WaterLevel(Data_BLKS_0400_GWL_2M)
#plt.title('Normalized Data: BLKS_0400_GWL_2M')
#plt.xlim(pd.Timestamp(2010,1,1),pd.Timestamp(2020,1,1)) 
    
#Filter wells with data in March, April,2019


# Filter wells with data in March, April,2019
#Ex3

def Filter_Autumn_Data(Data):
    df_Autumn = pd.DataFrame(columns=['Well', 'x', 'y', 'MeanGroundwaterLevel', 'LevelAutumn2018', 'Difference'])
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
                df_Autumn = df_Autumn.append(SpTi)
            except:
                pass

    return(df_Autumn)
  
#Ex 4

def Filter_Spring_Data(Data):
    df_Spring=pd.DataFrame(columns=['Well', 'x', 'y', 'MeanGroundwaterLevel2', 'LevelMarchApril2019', 'Difference'])
    StartSpring2019 = pd.Timestamp(2019,3,1)
    EndSpring2019 = pd.Timestamp(2019,4,30)
    for i in range(0,520):
        if Data[i].count()[0] > 1: # so that wells with only one measurement are not taken into account
            LevelsMarchApril=[]      
            for k in Data[i].index.tolist():
                if StartSpring2019 < Data[i].iloc[k,16] < EndSpring2019:
                    LevelsMarchApril.append(Data[i].iloc[k,18])         
            try:
                LevelsMarchApril2019 = statistics.mean(LevelsMarchApril)
                SpTi = pd.DataFrame([Data[i].iloc[0,3],Data[i].iloc[0,6], Data[i].iloc[0,7],Data[i].mean()[-2],LevelsMarchApril2019,LevelsMarchApril2019 - Data[i].mean()[-2]], index=['Well', 'x', 'y', 'MeanGroundwaterLevel2', 'LevelMarchApril2019','Difference'])
                SpTi = SpTi.transpose()
                df_Spring = df_Spring.append(SpTi)
            except:
                pass
    return(df_Spring)
   
#MAP the diference between March-April 2019 and the average groundwater level.
from pykrige.ok import OrdinaryKriging
import pykrige.kriging_tools as kt
import geopandas as gdp #Geospatial library

def Spatial_Map(df, filename):
    lons = np.array(df['x']) #lons =longitude
    lats = np.array(df['y']) #lats=lattitude
    data = np.array(df['Difference'])
    
    plt.figure()
    plt.scatter(lons, lats, 15, data, cmap = plt.cm.Blues)
    plt.xlabel("East")
    plt.ylabel("North")
    plt.title("Data Visualization")
    cbar = plt.colorbar()
    cbar.set_label("Data", labelpad=+1) #Why "labelpad+1" #minus, for example -100 will set the label "Data" more to the left side. If you set += then the label "Data" will be set more to the right. If you set = python wil read it like you would type +=
    plt.show()

    OK = OrdinaryKriging(lons, lats, data, variogram_model='spherical', nlags=25, verbose=True, enable_plotting=True) #To check spatial correlation #What does the verbose=True do?
    # z1, ss1 = OK.execute('grid', lons, lats)
    # xintrp, yintrp = np.meshgrid(grid_lon, grid_lat)
    # xintrp, yintrp = np.meshgrid(lons, lats)

    grid_x = np.linspace(150000, 250000, num = 100, endpoint = False)
    grid_y = np.linspace(160000, 220000, num = 100, endpoint = False)

    # Creates the kriged grid and the variance grid. Allows for kriging on a rectangular
    # grid of points, on a masked rectangular grid of points, or with arbitrary points.
    # (See OrdinaryKriging.__doc__ for more information.):

    z, ss = OK.execute('grid', grid_x, grid_y) # data: z and variance:ss 

    # Writes the kriged grid to an ASCII grid file:

    kt.write_asc_grid(grid_x, grid_y, z, filename="kriging_ordinary.asc") #Ordinary Kriging in matrix form

    kt.write_asc_grid(grid_x, grid_y, ss, filename="kriging_ordinary_var.asc") #Estimation variance in matrix form

    asc = pd.read_csv("kriging_ordinary.asc", header=None, skiprows=7, sep="\s+") 
    asc.shape #check that they are 70 rows and 80 columns #Why 70 rows and 80 columns?

    cu2 = np.array(asc) #pandas dataframe to ndarray conversion

    #Krigging map plot
    from descartes import PolygonPatch #PolygonPatch: Constructs a matplotlib patch from a geometric object, but what is a "matplotlibpatch"??

    gpo = gdp.read_file("C:\\Users\\Julio\\Desktop\\IUPWARE\\ENVIRONMENTAL PROGRAMMING\\Project Groundwater\\Data\\Groundwaterbodies_Oligocene\\")

    fig = plt.figure(figsize = (12,12))
    ax = fig.gca()

    a = plt.imshow(cu2, cmap=plt.cm.YlOrBr, extent=[150000,250000,160000,220000]) #gist_rainbow
    plt.grid(True)
    cbar = fig.colorbar(a, orientation='horizontal', pad=0.05)
    cbar.set_label("Anomaly in mTAW", labelpad=+1)
    plt.title('Anomaly of groundwater level - Kriging interpolation')
    plt.xlabel('East')
    plt.ylabel('North')
    ax.scatter(lons, lats, c='blue')
    for i in gpo['geometry']:
        ax.add_patch(PolygonPatch(i, fill=False, alpha=0.5, zorder=2, hatch='////')) #What does this line of code do?
    plt.show()
    #Save as PDF document
    fig.savefig(filename+".pdf", bbox_inches='tight')
    
#df = Filter_Spring_Data(Data)
#Spatial_Map(df)
