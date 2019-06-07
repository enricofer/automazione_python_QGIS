# -*- coding: utf-8 -*-
from qgis.core import QgsProcessing, QgsWkbTypes
from qgis.processing import alg

#dichiarazione generale dell'interfaccia utente dell'algoritmo
@alg(name="dettagli_layer", label="dettagli layer", group="customscripts", group_label=alg.tr("Custom Scripts"))
#dichiarazione dei widget di input ed output
@alg.input(type=alg.SOURCE, name="INPUT", label="Input layer", types=[QgsProcessing.TypeVectorAnyGeometry])
@alg.input(type=alg.FIELD, name="CAMPO", label="Campo da riassumere", parentLayerParameterName="INPUT")
@alg.input(type=alg.FILE_DEST, name="OUTPUT_HTML_FILE", label="Output HTML", fileFilter='HTML files (*.html)')

def algoritmo_di_processing(instance, parameters, context, feedback, inputs):
    """
    corpo della procedura di processing
    """

    def creaHTML(outputFile, algData):
        with open(outputFile, 'w', encoding='utf-8') as f:
            f.write('<html><head>')
            f.write('<meta http-equiv="Content-Type" content="text/html; \
                     charset=utf-8" /></head><body>')
            f.write('<p>Dati processati: ' + str(len(algData)) + '</p>')
            f.write('<p>Valori:</p>')
            f.write('<table>')
            for s in algData:
                f.write('<tr>')
                for attr in s:
                    f.write('<td>' + str(attr) + '</td>')
                f.write('</tr>')
            f.write('</table></body></html>')
    
    #raccolta dei parametri configurati dall'utente
    sorgente = instance.parameterAsSource(parameters, "INPUT", context)
    campi = instance.parameterAsFields(parameters, "CAMPO", context)
    destinazione = instance.parameterAsFileOutput(parameters, "OUTPUT_HTML_FILE", context)
    
    #processing
    valori = []
    for feat in sorgente.getFeatures():
        valori.append([feat.id(),feat[campi[0]]])
    creaHTML(destinazione,valori)
    
    #restituzione del risultato
    return {"OUTPUT_HTML_FILE": destinazione}