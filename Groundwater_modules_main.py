import matplotlib.pyplot as plt
import pandas as pd
import EnvironmentalProgrammingAsignment_Group1_Module as EPAG1M
from EnvironmentalProgrammingAsignment_Group1_Module import Fig_Evolution_WaterLevel
from EnvironmentalProgrammingAsignment_Group1_Module import GW_body_group
from EnvironmentalProgrammingAsignment_Group1_Module import Filter_Autumn_Data
from EnvironmentalProgrammingAsignment_Group1_Module import Filter_Spring_Data
from EnvironmentalProgrammingAsignment_Group1_Module import Spatial_Map
from matplotlib.backends.backend_pdf import PdfPages

#Reading the data
#ListWells_Oligocene.xlsx
userinput=input("Which file do you want to read?")
Data=EPAG1M.Read_Data(userinput)

##Ex1
FigEvolution=EPAG1M.Fig_Evolution_WaterLevel(Data)
FigEvolution.savefig("Normalized_data.pdf", bbox_inches='tight')

#Ex2
#Plotting the normalized data for each groundwater body from 2010-2020
Wells=pd.read_excel(userinput)
GW_body = ['BLKS_0400_GWL_1S','BLKS_0400_GWL_2S','BLKS_0400_GWL_1M','BLKS_0400_GWL_2M']
output = PdfPages("Evolution_groundwaterbodies.pdf")
for i in range(len(GW_body)):
    figure = Fig_Evolution_WaterLevel(GW_body_group(Wells, GW_body[i], Data))
    plt.title('Normalized Data: '+GW_body[i])
    plt.xlim(pd.Timestamp(2010,1,1),pd.Timestamp(2020,1,1))
    output.savefig(figure)
output.close()

###Ex3
df_Autumn=Filter_Autumn_Data(Data)
Spatial_Map(df_Autumn, "Autumn2018")


###Ex 4
df_Spring=Filter_Spring_Data(Data)
Spatial_Map(df_Spring, "Spring2019")
