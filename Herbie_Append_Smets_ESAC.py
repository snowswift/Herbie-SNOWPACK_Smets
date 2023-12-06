#!/usr/bin/env python
# coding: utf-8

# In[2]:


from herbie import Herbie
from datetime import datetime, timedelta
import math
from herbie import FastHerbie
import pandas as pd
    
start_time_str = '2023-11-30 00:00:00'
startrun = 23 # first forecast hour in run, does not have to start at 0
maxrun = 25 # last forecast hour in run, to get 48hr model: maxrun = 49

file_name_list = ['/home/bran/SNOWPACK/input/CUES/CUES.smet', '/home/bran/SNOWPACK/input/Tioga/Tioga.smet', '/home/bran/SNOWPACK/input/Rock_Creek/Rock_Creek.smet']
ll = [(-119.028661,37.645588),(-119.256899,37.935258),(-118.726413,37.452796)] # lat/long for selected HRRR grid points. lat/long order: CUES, Tioga, Rock_Creek
ss1 = ":TMP:2 m|:RH:2 m" # 2m readings
ss2 = ":WIND:10 m" # 10m readings
ss3 = ":GUST:surface|:DSWRF:surface|:DLWRF:surface|:ULWRF:surface|USWRF:surface|:APCP:surface:(?:0-1|[1-9]\d*-\d+)*" # surf readings minus precip

def append_data(y1_d, y2_d, y3_d, output_timestamp_str):
    
    timeindex = i - startrun
    t2m = y1_d['data_vars']['t2m']['data'][data_index][timeindex]
    r2 = y1_d['data_vars']['r2']['data'][data_index][timeindex]
    wind10 = y2_d['data_vars']['si10']['data'][data_index][timeindex]
    gust = y3_d['data_vars']['gust']['data'][data_index][timeindex]
    dsw = y3_d['data_vars']['dswrf']['data'][data_index][timeindex]
    dlw = y3_d['data_vars']['dlwrf']['data'][data_index][timeindex]
    ulw = y3_d['data_vars']['ulwrf']['data'][data_index][timeindex]
    usw = y3_d['data_vars']['uswrf']['data'][data_index][timeindex]
    hrprecip = y3_d['data_vars']['tp']['data'][data_index][timeindex]
    if i==0:
        hrpreciplast = 0
    else:
        hrpreciplast = y3_d['data_vars']['tp']['data'][data_index][timeindex-1]
    hrprecipfile = hrprecip - hrpreciplast
        
    t2m_formatted = round(t2m, 1) # 2nd parameter is number of decimals
    r2_formatted = round(r2)
    gust_formatted = round(gust, 1)
    wind10_formatted = round(wind10, 1)
    dsw_formatted = round(dsw)
    dlw_formatted = round(dlw)
    ulw_formatted = round(ulw)
    usw_formatted = round(usw)
    hrprecip_formatted = round(hrprecipfile, 1)
    
    file_name = file_name_list[j]
    
    if i == startrun:
        print("Ignore This")
        
    else:
    
        new_line_str = f"{output_timestamp_str} {t2m_formatted} {r2_formatted} {gust_formatted} {wind10_formatted} {dsw_formatted} {dlw_formatted} {ulw_formatted} {usw_formatted} {hrprecip_formatted} 0.0\n"
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

DATES = pd.date_range(
    start = start_time_str,
    periods=1,
    freq="24H")

fxx = range(startrun,maxrun) 

FH = FastHerbie(DATES, model="hrrr", fxx=fxx)
FH
print('querying data for 2 m')
ds1 = FH.xarray(ss1, remove_grib=False)
y1=ds1.herbie.nearest_points(points=ll)
y1_d = y1.to_dict()

print('querying data for 10 m')
ds2 = FH.xarray(ss2, remove_grib=False)
y2=ds2.herbie.nearest_points(points=ll)
y2_d = y2.to_dict()

print('querying data for surface')
ds3 = FH.xarray(ss3, remove_grib=False)
y3=ds3.herbie.nearest_points(points=ll)
y3_d = y3.to_dict()

for i in range(startrun,maxrun): # iterating data for each hour
    dt = datetime.fromisoformat(start_time_str)
    dt_query_str = dt.strftime('%Y-%m-%d %H:%M')
    output_timestamp = dt + timedelta(hours=i)
    output_timestamp_str = output_timestamp.strftime('%Y-%m-%dT%H:%M')
    hours_offset = i
    
    for j in range(3): # printing to smet for each station, range should match number of stations, 0->n
        data_index = j
        append_data(y1_d, y2_d, y3_d, output_timestamp_str)
        

        
print("done")



