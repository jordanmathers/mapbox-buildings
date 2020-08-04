from ast import literal_eval
import geojson as gj
import json


def logToGeojson(fileOpen, fileSave):
    
    with open(fileOpen) as f:
        content = f.readlines()

    def convertType(x):
        try:
            return literal_eval(x)
        except:
            return x

    newContent = []
    for x in content:
        if x[:6] == 'Mapbox':
            newContent.append(convertType(x[35:].strip()))
        else:
            newContent.append(convertType(x[4:].strip()))

    geomType = []
    height = []
    minHeight = []
    ids = []
    contentCoords = []

    itemCoords = []
    coords = []
    count = 0
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
            if count == 0:
                contentCoords.append(itemCoords)
                itemCoords = []
                height.append(line)
                count += 1
            elif count == 1:
                minHeight.append(line)
                count += 1
            else:
                ids.append(line)
                count = 0

    features = []
    for t, h, m, i, c in zip(geomType, height, minHeight, ids, contentCoords):
        if t == 'Polygon':
            geom = gj.Polygon([c])
            feature = gj.Feature(geometry=geom, properties={'id': i, 'height': h, 'min_height': m})
            features.append(feature)

    featureCollection = gj.FeatureCollection(features)

    with open(f'{fileSave}.geojson', 'w') as f:
        gj.dump(featureCollection, f)




