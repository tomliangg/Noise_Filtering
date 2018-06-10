import xml.etree.ElementTree as ET
import pandas as pd

df = pd.DataFrame(columns=['lat', 'lon'])

#<trkpt lat="49.28022235" lon="-123.00543652"><ele>71.0</ele><time>2017-04-18T20:26:20.000Z</time><course>272.8</course><speed>1.5</speed><geoidheight>-15.0</geoidheight><src>gps</src><sat>7</sat><hdop>0.6</hdop><vdop>0.7</vdop><pdop>1.0</pdop></trkpt>

tree = ET.parse('walk1.gpx')
root = tree.getroot()
#root has two children tags: 1) time 2) trk
#trk has trkseg tag
#trkseg has trkpt tag which holds the lat and lon info

i = 0
for child in root[1][0]:
    df.loc[i] = [float(child.attrib['lat']), float(child.attrib['lon'])]
    i += 1

print (df)

df_shifted = df.shift(periods=-1)
df_diff = abs(df - df_shifted)
print (df_diff.sum())
"""
output of the df.head()
   lat            lon
0    49.28015799  -123.00528338
1    49.28022235  -123.00543652
2    49.28023114  -123.00560132
3     49.2803905   -123.0064075
4    49.28021094  -123.00596532
5     49.2803988   -123.0061052
..           ...            ...
119  49.275721 -123.018331
120  49.275859 -123.018304
"""