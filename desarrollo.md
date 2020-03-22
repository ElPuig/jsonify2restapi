# Aventurillas encontradas durante la migración.

## 20/3/2020 Primera importación con un conjunto de datos reales

A partir de un backup del centro se han exportado 12151 ficheros json que son una pequeña parte de los contenidos totales.

En la máquina en la que trabajo jsonify2restapi.py tarda algo más de 2h en procesar todos los ficheros. El resultado es:

Ficheros importados: 6559
Ficheros no importados: 5592

Entre los ficheros no importados se encuentran los siguientes casos:

- Objetos que no son de uno de los tipos nativos de Plone. -> Se ignoran.
- Objetos de tipo *File* que no tienen serializados los datos. Por alguna razón no tienen el campo *_datafield_file*. Curiosamente estos ficheros JSON tienen el campo *_old_paths* que los ficheros con datos serializados no tienen. Quizás jsonify2restapi los pueda descargar del Plone original y subir a la nueva instancia. Los primeros de ellos: {29, 30, 31, 32}.json
- Objetos de tipo *Folder* que por alguna razón no quieren cargar. El primero de ellos: 345.json. No he encontrado diferencia entre los objetos de tipo *Folder* que se importan sin problemas y los que no se importan. Pero al no crearse la carpeta no se puede importar ninguno de los objetos que contiene. Quizás jsonify2restapi pueda reintentar la creación de estas carpetas problemáticas de un modo más básico: tipo e id.


Medidas:

- Objetos *File* que no tengan los datos serializados. Se intentarán descargar desde el sitio original y subir al nuevo. Ok, resuelto.
- Objetos *Folder* que por alguna razón no quieren cargar. Tienen vacío el campo *title*, en tal caso se copia el *id*. Ok, resuelto.

## 22/3/2020

Si se intentan descargar ficheros desde el servidor original, conviene tener iniciada la sesión con el usuario administrador para que se puedan descargar.

