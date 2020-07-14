#%%

from ast import literal_eval
import geojson as gj
import json

fileOpen = r"C:\Users\jmathers\Documents\Programming\Repositories\Mapbox-Buildings\01.log"
fileSave = r"C:\Users\jmathers\Documents\Programming\Repositories\Mapbox-Buildings\data\test.geojson"

with open(fileOpen) as f:
    content = f.readlines()

def convertType(x):
    try:
        return literal_eval(x)
    except:
        return x

newContent = []
for x in content:
    if x[:5] == 'build':
        newContent.append(convertType(x[14:].strip()))
    else:
        newContent.append(convertType(x[4:].strip()))


geomType = []
height = []
minHeight = []
contentCoords = []

itemCoords = []
coords = []
add = True
for line in newContent:
    if isinstance(line, str):
        geomType.append(line)
    elif isinstance(line, float):
        if len(coords) <= 1:
            coords.append(line)
        else:
            itemCoords.append(coords)
            coords = [line]
    elif isinstance(line, int):
        coords = []
        if add:
            contentCoords.append(itemCoords)
            itemCoords = []
            height.append(line)
            add = False
        else:
            minHeight.append(line)
            add = True

features = []
for t, h, m, c in zip(geomType, height, minHeight, contentCoords):
    if t == 'Polygon':
        geom = gj.Polygon([c])
        feature = gj.Feature(geometry=geom, properties={'height': h, 'min_height': m})
        features.append(feature)

featureCollection = gj.FeatureCollection(features)

with open(fileSave, 'w') as f:
    gj.dump(featureCollection, f)
