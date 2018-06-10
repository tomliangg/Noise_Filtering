from math import cos, asin, sqrt


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a)) #2*R*asin...  distance in KM

print('new')
lat1 = 49.28015799
lon1 = -123.00528338
lat2 = lat1 + 0.016341
lon2 = lon1 + 0.029491
print (distance(lat1, lon1, lat2, lon2))