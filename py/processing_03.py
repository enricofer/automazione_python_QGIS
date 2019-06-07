# -*- coding: utf-8 -*-
from qgis.core import QgsProcessing, QgsVectorFileWriter, QgsVectorLayerExporter 
from qgis.processing import alg

#dichiarazione generale dell'interfaccia utente dell'algoritmo
@alg(name="salva_in_geopackage", label="salva in geopackage", group="customscripts", group_label=alg.tr("Custom Scripts"))
#dichiarazione dei widget di input ed output

@alg.input(type=alg.MULTILAYER, name="LAYERS", label="Layers da includere", layerType=QgsProcessing.TypeVectorAnyGeometry)
@alg.input(type=alg.FILE_DEST, name="OUTPUT_GEOPACKAGE_FILE", label="Output GEOPACKAGE", fileFilter='GEOPACKAGE files (*.gpkg)')

def algoritmo_di_processing(instance, parameters, context, feedback, inputs):
    """
    corpo della procedura di processing
    """
    
    #raccolta dei parametri configurati dall'utente
    layers_sorgenti = instance.parameterAsLayerList(parameters, "LAYERS", context)
    gpkgPath = instance.parameterAsFile(parameters, "OUTPUT_GEOPACKAGE_FILE", context)
    layers_inclusi=[]
    primo = True
    print(gpkgPath)
    #processing
    for lyr in layers_sorgenti:
        options = QgsVectorFileWriter.SaveVectorOptions()
        if primo:
            primo = False
        else:
            options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer 
            options.EditionCapability = QgsVectorFileWriter.CanAddNewLayer 
            options.layerName = lyr.name() #"_".join(lyr.name().split(' '))
        _writer = QgsVectorFileWriter.writeAsVectorFormat(lyr, gpkgPath, options)
        if _writer:
            layers_inclusi.append([lyr.name(),_writer])
            print(lyr.name(), _writer)
    
    #restituzione del risultato
    return {"OUTPUT": layers_inclusi}
