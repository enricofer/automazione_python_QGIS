# -*- coding: utf-8 -*-
from qgis.core import QgsProcessing, QgsWkbTypes
from qgis.processing import alg

#dichiarazione generale dell'interfaccia utente dell'algoritmo
@alg(name="duplica_layer", label="duplica layer", group="customscripts", group_label=alg.tr("Custom Scripts"))
#dichiarazione dei widget di input ed output
@alg.input(type=alg.SOURCE, name="INPUT", label="Input layer", types=[QgsProcessing.TypeVectorPolygon])
@alg.input(type=alg.NUMBER, name="AREA_MIN", label="Area minima (ettari)")
@alg.input(type=alg.SINK, name="OUTPUT", label="Output layer")

def algoritmo_di_processing(instance, parameters, context, feedback, inputs):
	"""
	corpo della procedura di processing
	"""
	
    #raccolta dei parametri configurati dall'utente
	sorgente = instance.parameterAsSource(parameters, "INPUT", context)
	areaMinima = instance.parameterAsDouble(parameters, "AREA_MIN", context)
	(destinazione, dest_id) = instance.parameterAsSink(
		parameters,
		"OUTPUT",
		context,
		sorgente.fields(),
		sorgente.wkbType(),
		sorgente.sourceCrs()
	)
	
    #processing
	for feat in sorgente.getFeatures():
		geometry = feat.geometry()
		if geometry.area() > areaMinima*10000:
			destinazione.addFeature(feat)
	
	#restituzione del risultato
	return {"OUTPUT": dest_id}
