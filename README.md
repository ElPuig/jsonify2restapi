# jsonify2restapi

Este script ayuda en la migración de contenido de una versión antigua de Plone (que soporte collective.jsonify - https://github.com/collective/collective.jsonify) a una versión nueva (que soporte plone.restapi - https://plonerestapi.readthedocs.io/en/latest/).

La migración consiste en instalar collective.jsonify en la instancia de Plone antigua (o bien actualizar la versión antigua hasta la última versión 4.x e instalar allí collective.jsonify) para exportar los contenidos a formato JSON.

Después el script jsonify2restapi puede enviar estos contenidos a una instancia nueva de Plone 5 que soporte plone.restapi.

En los ficheros **error.log** e **imported.log** se registrará información sobre los contenidos que han provocado un error y aquellos que se ha podido importar en el nuevo Plone.

La importación no es perfecta, entre otras cuestiones:

 - Solo se importan los tipos básicos de Plone
 - Se supone que se utiliza el workflow por defecto
 - Se pierde la vista por defecto a no ser que el elemento tenga por id index_html
 - Todavía no importa los permisos de la compartición de contenidos

 ## Instalación
 
 Esta herramienta utiliza pipenv - https://pipenv-fork.readthedocs.io/en/latest/

```
pipenv --python 3
pipenv shell
```

## Authors

* **Victor Carceler**

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.