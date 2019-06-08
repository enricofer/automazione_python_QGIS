from qgis.processing import alg

from PyQt5.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsFields,QgsField,QgsFeature,QgsGeometry, QgsWkbTypes, QgsRaster)

@alg(name="measure_Elevation_along_lines", label="Measure DTM elevation along lines", group="customscripts", group_label=alg.tr("Custom Scripts"))
@alg.input(type=alg.RASTER_LAYER, name='DTM_LAYER', label="Layer DTM")
@alg.input(type=alg.SOURCE, name='INPUT_LAYER', label="Input layer", types=[QgsProcessing.TypeVectorLine])
@alg.input(type=alg.DISTANCE, name="MEASURE_VALUE", label="Measure step size", default=50.0) 
@alg.input(type=alg.SINK, name="OUTPUT_LAYER", label="Output layer")

def processAlgorithm(instance, parameters, context, feedback, inputs):
    """
    Algoritm to extract elevation on DTM from linestring paths at specified measure step
    """


    vectorLayer = instance.parameterAsSource(parameters, "INPUT_LAYER", context)
    dtmLayer = instance.parameterAsRasterLayer(parameters, "DTM_LAYER", context)
    measureStep = instance.parameterAsInt (parameters, "MEASURE_VALUE", context)


    fields=QgsFields()
    fields.append(QgsField('id_poly', QVariant.Int))
    fields.append(QgsField('elevation', QVariant.Double))
    fields.append(QgsField('step', QVariant.Double))


    (sink, dest_id) = instance.parameterAsSink(parameters, "OUTPUT_LAYER", context, fields, QgsWkbTypes.Point, vectorLayer.sourceCrs())


    for feat in vectorLayer.getFeatures():
        currentLen = 0
        while currentLen < feat.geometry().length():
            node = feat.geometry().interpolate(currentLen)
            if node:
                point = node.asPoint()
                elevFeat = QgsFeature(fields)
                elevValue = dtmLayer.dataProvider().identify(point, QgsRaster.IdentifyFormatValue).results()[1]
                elevFeat['elevation'] = elevValue
                elevFeat['step'] = currentLen
                elevFeat['id_poly'] = feat.id()
                elevGeom = QgsGeometry.fromPointXY(point)
                elevFeat.setGeometry(elevGeom)
                sink.addFeature(elevFeat, QgsFeatureSink.FastInsert)
            currentLen += measureStep

    return {"OUTPUT_LAYER": dest_id,}
    fields.append(QgsField('elevation', QVariant.Double))
    fields.append(QgsField('step', QVariant.Double))


    (sink, dest_id) = instance.parameterAsSink(parameters, "OUTPUT_LAYER", context, fields, QgsWkbTypes.Point, vectorLayer.sourceCrs())


    for feat in vectorLayer.getFeatures():
        currentLen = 0
        while currentLen < feat.geometry().length():
            node = feat.geometry().interpolate(currentLen)
            if node:
                point = node.asPoint()
                elevFeat = QgsFeature(fields)
                elevValue = dtmLayer.dataProvider().identify(point, QgsRaster.IdentifyFormatValue).results()[1]
                elevFeat['elevation'] = elevValue
                elevFeat['step'] = currentLen
                elevFeat['id_poly'] = feat.id()
                elevGeom = QgsGeometry.fromPointXY(point)
                elevFeat.setGeometry(elevGeom)
                sink.addFeature(elevFeat, QgsFeatureSink.FastInsert)
            currentLen += measureStep

    return {"OUTPUT_LAYER": dest_id,}
