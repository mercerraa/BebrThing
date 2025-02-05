# Export data from geopackage to geojson
# Selects objects by attribute for export
# Each selection saved as seperate file as adding on during export creates one, large object rather than individual objects
# Concatenates each export into one file
# Intended use: Bebyggelseregistret
#  
import os
from qgis.core import Qgis
from qgis.core import QgsProject
from qgis.utils import iface

def getActive():
    '''Gets the active layer and retuns pyqgis object layer'''
    layer = qgis.utils.iface.activeLayer()
    print(f'Layer ID: {layer.id()}')
    print(f'Feature count: {layer.featureCount()}')
    for field in layer.fields():
        print(field.name(), field.type())
    return layer

def addVardef(filename, line):
    '''Prepends variable definition to head of file, making geoJson object an importable variable'''
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)
    return

def exportGeojson(layer, field, value, path, geometry):
    '''Exports selected objects to GeoJson and then calls addVardef to prepend variable definition'''
    selectText = f"\"{field}\" ilike \'%{value}%\'"
    print(selectText)
    layer.selectByExpression(selectText)
    name = geometry + value
    filename = os.path.join(path, name)
    QgsVectorFileWriter.writeAsVectorFormat(layer, f'{filename}', 'utf-8', QgsCoordinateReferenceSystem('EPSG:4326'), 'GeoJSON', layerOptions=['COORDINATE_PRECISION=8'], onlySelected=True)
    line = f"let {geometry}{value} = "
    addVardef(filename + '.geojson', line)
    print('Done.')
    return

def exportUniqueGeojson(layer, field, path, geometry):
    idx = layer.fields().indexOf(field)
    unique_values = layer.uniqueValues(idx)
    print(f'Found values: {unique_values}')
    for value in unique_values:
        layer.selectByExpression(f"{field}='{value}'")
        name = geometry + value
        filename = os.path.join(path, name)
        QgsVectorFileWriter.writeAsVectorFormat(layer, f'{filename}', 'utf-8', QgsCoordinateReferenceSystem('EPSG:4326'), 'GeoJSON', layerOptions=['COORDINATE_PRECISION=8'], onlySelected=True)
        line = f"let {geometry}{value} = "
        addVardef(filename + '.geojson', line)
    print('Done.')
    return

lanList = [
    "Blekinge", "Dalarna", "Gotland",
    "Gävleborg", "Halland", "Jämtland",
    "Jönköping", "Kalmar", "Kronoberg",
    "Norrbotten", "Skåne", "Stockholm",
    "Södermanland", "Uppsala", "Värmland",
    "Västerbotten", "Västernorrland", "Västmanland",
    "Västra Götaland", "Örebro", "Östergötland"]

path = QgsProject.instance().readPath("./")
os.chdir(path)

layer = getActive()
if layer.geometryType() == QgsWkbTypes.PointGeometry:
    geometry = "point"
elif layer.geometryType() == QgsWkbTypes.PolygonGeometry:
    geometry = "polygon"
elif layer.geometryType() == QgsWkbTypes.LineGeometry:
    geometry = "line"
else :
    geometry = ""

#exportUniqueGeojson(layer, 'lan', path, geometry)

for lan in lanList: exportGeojson(layer, 'lan', lan, path, geometry)
