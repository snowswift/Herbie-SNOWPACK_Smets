from herbie import Herbie
H = Herbie("2023-11-06 12:00",model="hrrr",fxx=6,save_dir="~/ESAC_herbiedata")
ss = ":TMP:2 m|:RH:2 m|:WIND:10 m|:.GRD:10 m|:DSWRF:surface|:DLWRF:surface|:ULWRF:surface|USWRF:surface|:APCP:surface"
ss1 = ":TMP:2 m|:RH:2 m" # 2m readings
ss2 = ":WIND:10 m|:.GRD:10 m" # 10m readings
ss3 = ":DSWRF:surface|:DLWRF:surface|:ULWRF:surface|USWRF:surface|:APCP:surface" # surf readings
#print(H.inventory(searchString=":TMP:2 m|:RH:2 m|:WIND:10 m|:.GRD:10 m|:DSWRF:surface|:DLWRF:surface|:ULWRF:surface|USWRF:surface|:APCP:surface"))
# not sure about winds
ds = H.xarray(ss1, remove_grib=False)
ll = [(-119.02,37.64),(-119.25,37.91),(-118.73,37.45)]
y=ds.herbie.nearest_points(points=ll)
# print(ds)
print(y)
