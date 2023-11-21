#!/usr/bin/env python
# coding: utf-8

# In[6]:


from herbie import Herbie
from datetime import datetime, timedelta
import math
from herbie import FastHerbie
import pandas as pd
    
file_name = '/home/bran/SNOWPACK/input/Tioga/Tioga_test.smet'
data_index = 1 #index is station lat/long, starts at 0
start_time_str = '2023-10-26 00:00:00'
ss = ":TMP:2 m|:RH:2 m|:WIND:10 m|:.GRD:10 m|:DSWRF:surface|:DLWRF:surface|:ULWRF:surface|USWRF:surface|:APCP:.*:(?:0-1[1-9]\d*-\d+) hour"
ss1 = ":TMP:2 m|:RH:2 m" # 2m readings
ss2 = ":WIND:10 m|:.GRD:10 m" # 10m readings
ss3 = ":DSWRF:surface|:DLWRF:surface|:ULWRF:surface|USWRF:surface|:APCP:surface:(?:0-1|[1-9]\d*-\d+)*" # surf readings minus precip
#ss4 = f":APCP:surface:{i-1}-{i} h*" #hourly precip
ll = [(-119.02,37.64),(-119.25,37.91),(-118.73,37.45)] # lat/long order: CUES, Tioga, Rock_Creek
maxrun = 12 # to get 48hr model: maxrun = 49

DATES = pd.date_range(
    start = start_time_str,
    periods=1,
    freq="24H")

fxx = range(0,maxrun)

FH = FastHerbie(DATES, model="hrrr", fxx=fxx)
FH
ds1 = FH.xarray(ss1, remove_grib=False)
y1=ds1.herbie.nearest_points(points=ll)
print('querying data for 2 m')
y1_d = y1.to_dict()
ds2 = FH.xarray(ss2, remove_grib=False)
y2=ds2.herbie.nearest_points(points=ll)
print('querying data for 10 m')
y2_d = y2.to_dict()
ds3 = FH.xarray(ss3, remove_grib=False)
y3=ds3.herbie.nearest_points(points=ll)
print('querying data for surface')
y3_d = y3.to_dict()

def append_data(y1_d, y2_d, y3_d, output_timestamp_str):
    t2m = y1_d['data_vars']['t2m']['data'][data_index][i]
    r2 = y1_d['data_vars']['r2']['data'][data_index][i]
    maxwind10 = y2_d['data_vars']['si10']['data'][data_index][i]
    uwind10 = y2_d['data_vars']['u10']['data'][data_index][i]
    vwind10 = y2_d['data_vars']['v10']['data'][data_index][i]
    wind10 = math.sqrt(uwind10**2 + vwind10**2)
    dsw = y3_d['data_vars']['dswrf']['data'][data_index][i]
    dlw = y3_d['data_vars']['dlwrf']['data'][data_index][i]
    ulw = y3_d['data_vars']['ulwrf']['data'][data_index][i]
    usw = y3_d['data_vars']['uswrf']['data'][data_index][i]
    hrprecip = y3_d['data_vars']['tp']['data'][data_index][i]
        
    t2m_formatted = round(t2m, 1) #2nd parameter is number of decimals
    r2_formatted = round(r2)
    maxwind10_formatted = round(maxwind10, 1)
    wind10_formatted = round(wind10, 1)
    dsw_formatted = round(dsw)
    dlw_formatted = round(dlw)
    ulw_formatted = round(ulw)
    usw_formatted = round(usw)
    hrprecip_formatted = round(hrprecip, 1)
    
    new_line_str = f"{output_timestamp_str} {t2m_formatted} {r2_formatted} {maxwind10_formatted} {wind10_formatted} {dsw_formatted} {dlw_formatted} {ulw_formatted} {usw_formatted} 0.0\n"
    with open(file_name, 'r') as f:
        lines = f.readlines()
        print(type(lines))
        print(len(lines))
        new_lines = lines
        found= False
        for idx, line in enumerate(lines):
            if line[:16] == output_timestamp_str:
                new_lines[idx] = new_line_str
                found = True
                break
        if not found:
            new_lines += [new_line_str]
    print(len(new_lines))
    with open(file_name, 'w') as f:
        f.writelines(new_lines)
        
print("Append Data Defined")


#ss4 = ":APCP:surface:(?:0-1|[1-9]\d*-\d+)*" #hourly precip
#
#print('querying data for precip')
#ds4 = FH.xarray(ss4, remove_grib=False)
#y4=ds4.herbie.nearest_points(points=ll)
#y4_d = y4.to_dict()

for i in range(maxrun):
    dt = datetime.fromisoformat(start_time_str)
    dt_query_str = dt.strftime('%Y-%m-%d %H:%M')
    output_timestamp = dt + timedelta(hours=i)
    output_timestamp_str = output_timestamp.strftime('%Y-%m-%dT%H:%M')
    hours_offset = i
    #H = Herbie(start_time_str,model="hrrr",fxx=hours_offset,save_dir="~/ESAC_herbiedata")
    #print(H.inventory(searchString=":TMP:2 m|:RH:2 m|:WIND:10 m|:.GRD:10 m|:DSWRF:surface|:DLWRF:surface|:ULWRF:surface|USWRF:surface|:APCP:surface"))
    # not sure about winds
    
    
    append_data(y1_d, y2_d, y3_d, output_timestamp_str)


# In[3]:



# In[7]:


# hm2 = FH.inventory(searchString=ss2)
# print(hm2)


# In[ ]:




