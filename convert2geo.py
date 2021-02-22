#%%

from ast import literal_eval
import geojson as gj
import json


def logToGeojson(fileOpen, fileSave):
    
    with open(fileOpen) as f:
        content = f.readlines()

    content = literal_eval(content[0])

    features = []
    for x, y, z in zip(*content):
        if z == 'Polygon':
            feat = gj.Feature(geometry=gj.Polygon(x), properties={'id': y})
            features.append(gj.Feature(geometry=gj.Polygon(x), properties={'id': y}))
        elif z == 'MultiPolygon':
            features.append(gj.Feature(geometry=gj.MultiPolygon(x), properties={'id': y}))

    featureCollection = gj.FeatureCollection(features)

    with open(f'{fileSave}.geojson', 'w') as f:
        gj.dump(featureCollection, f) 


