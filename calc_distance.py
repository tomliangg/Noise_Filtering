import sys
import xml.etree.ElementTree as ET
import pandas as pd
from math import cos, asin, sqrt
from pykalman import KalmanFilter
import numpy as np

def get_data(input_filename):
    #input an XML/gpx file
    #return a DF
    #check testParse.py to understand how this function works
    df = pd.DataFrame(columns=['lat', 'lon'])
    tree = ET.parse(input_filename)
    root = tree.getroot()
    i = 0
    for child in root[1][0]:
        df.loc[i] = [float(child.attrib['lat']), float(child.attrib['lon'])]
        i += 1
    return df

def distance(points):
    #return the distance in meters
    points_shifted = points.shift(periods=-1)
    points_diff = abs(points - points_shifted)
    total_diff = points_diff.sum()
    return distanceOf2Points(points['lat'][0], points['lon'][0], points['lat'][0] + total_diff['lat'], points['lon'][0] + total_diff['lon'])

def distanceOf2Points(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a)) #2*R*asin...  distance in KM

def smooth(points):
    kf = KalmanFilter(
        initial_state_mean = points.iloc[0],
        observation_covariance = np.diag([0.5, 0.5]) ** 2, # TODO: shouldn't be zero
        transition_covariance = np.diag([0.3, 0.3]) ** 2, # TODO: shouldn't be zero
        transition_matrices = [[1, 0], [0, 1]] # TODO
    )
    kalman_smoothed, _ = kf.smooth(points)
    df = pd.DataFrame(data=kalman_smoothed, columns=['lat', 'lon'])
    return df


def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')


def main():
    points = get_data(sys.argv[1])
    print('Unfiltered distance: %0.2f' % (distance(points),))
    
    smoothed_points = smooth(points)
    print('Filtered distance: %0.2f' % (distance(smoothed_points),))
    output_gpx(smoothed_points, 'out.gpx')
   

if __name__ == '__main__':
    main()