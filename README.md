# Distributed Search Engine with Machine Learning

## Integrantes:
- Alben Luis Urquiza Rojas C412
- Frank Abel Blanco Gómez C412
- Karel Díaz Vergara C412

## Resumen
Los buscadores son programas o aplicaciones que colectan información que, según sea el caso, puede ser de manera local, en la red o en internet. Una vez colectada esta información es procesada y almacenada inteligentemente dentro de una base de datos a la cual puede acceder el buscador. A partir de esta base de datos entonces, desde el buscador y utilizando unos términos de búsqueda, se pueden recuperar los documentos que contengan información relevante y relacionada con lo que se busca. Existen buscadores para acceder a información en Internet o de manera local.  

El proyecto que se propone tiene como propósito implementar un buscador de archivos distribuidos en varias computadoras localizando los documentos a partir de un patrón de búsqueda y permitiendo el acceso a los documentos identificados. A diferencia de un buscador tradicional, en el buscador que se proyecta, cualquier computadora que se incorpore al sistema tendrá la capacidad de proveer documentos que puedan ser localizados y accedidos desde otras máquinas del sistema. De igual manera desde cualquier máquina se podrán realizar las búsquedas. El sistema deberá estar preparado para que la salida de una máquina del sistema, en cualquier momento (por ejemplo mientras se está accediendo a ella) no cause fallas o inconsistencias en el sistema.  

Además nos enfocaremos en clasificar los documentos, algo así como un data clustering de forma tal que podamos reducir el espacio de búsqueda del search engine, y utilizaremos ténicas de natural language preprocessing para hallar la similitud de un documento con la query, apoyándonos en modelos preentrenados como lo son glove y word2vec, además de usar un modelo probabilístico o el vectorial(que es más sencillo) en dependencia de la complejidad.
