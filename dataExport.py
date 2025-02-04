# Export data from geopackage to geojson
# Selects objects by attribute for export
# Each selection saved as seperate file as adding on during export creates one, large object rather than individual objects
# Concatenates each export into one file
# Intended use: Bebyggelseregistret
#  
from qgis.core import Qgis
from qgis.core import QgsProject
from qgis.utils import iface

def getActive():
    '''Sets the active layer as variable name, e.g. layer1 = getActive()'''
    layer = qgis.utils.iface.activeLayer()
    print(f'Layer ID: {layer.id()}')
    print(f'Feature count: {layer.featureCount()}')
    for field in layer.fields():
        print(field.name(), field.type())
    return layer

def selectFilterExpWord(layer, column, word, iter = False, shell = False):
    '''select objects from layer by searching for a string in an attribute column. Returns either a list of objects or an iterator'''
    selection = []
    request = QgsFeatureRequest().setFilterExpression(' "{}" = \'{}\' '.format(column, str(word)))
    iterator = layer.getFeatures(request)
    if iter == True: 
        return iterator
    else: 
        for found in iterator:
            if shell == True: print(found)
            selection.append(found)
            layer1.select(found.id())
        return selection

def addVardef(filename, line):
    '''Prepends variable definition to head of file, making geoJson object an importable variable'''
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)
    return

def exportGeojson(layer, filename, porp, lan):
    '''Exports selected objects to GeoJson and then calls addVardef to prepend variable definition'''
    QgsVectorFileWriter.writeAsVectorFormat(layer, f'{filename}', 'utf-8', QgsCoordinateReferenceSystem('EPSG:4326'), 'GeoJSON', layerOptions=['COORDINATE_PRECISION=8'], onlySelected=True)
    line = f"let {porp}{lan} = "
    addVardef(filename, line)

porp = "point"
# porp = "polygon"
lanList = [
    "Blekinge", "Dalarna", "Gotland",
    "Gävleborg", "Halland", "Jämtland",
    "Jönköping", "Kalmar", "Kronoberg",
    "Norrbotten", "Skåne", "Stockholm",
    "Södermanland", "Uppsala", "Värmland",
    "Västerbotten", "Västernorrland", "Västmanland",
    "Västra Götaland", "Örebro", "Östergötland"]

for lan in lanList:
    

