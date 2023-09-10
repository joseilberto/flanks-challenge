[![cov](https://github.com/joseilberto/flanks-challenge/blob/main/coverage.svg)](https://github.com/joseilberto/flanks-challenge/actions)

# FLANKS – Prueba Técnica 2023

En esta prueba queremos evaluar principalmente dos cosas:

- Tu habilidad para resolver un problema clásico de scraping
- Tus habilidades para comprender un problema y plantear una solución de software.
- Tus habilidades para organizar y testear código.

El objetivo de la prueba es crear un sistema para extraer y mantener una base de datos de
SICAVS. La información que nos interesa de cada una es la siguiente:

- Nombre
- Nº Registro oficial
- Fecha registro oficial
- Domicilio
- Capital social inicial
- Capital máximo estatutario
- ISIN
- Fecha último folleto

Todos estos datos pueden obtenerse del portal de la CNMV:
[<https://www.cnmv.es/Portal/Consultas/MostrarListados.aspx?id=18>](<https://www.cnmv.es/Portal/Consultas/MostrarListados.aspx?id=18>)

Te pedimos que nos entregues un repositorio de código privado que contenga:

- Un fichero docker-compose.yml para orquestar los siguientes contenedores
- Un contenedor que al ser lanzado extraiga/actualice los datos en el modelo de datos de las SICAV desde el portal de la CNMV.
- Un contenedor con la base de datos (mongodb) donde se persistirán los datos.
- Un contenedor que al lanzarlo corra todos los tests necesarios para comprobar que el sistema funciona. Este contenedor, idealmente, debería usar la misma base de código que el crawler.
- Un README.md con todo lo necesario para poder ejecutar los tests y el crawler periódicamente.

El sistema debe asumir que el contenedor de actualización se ejecutará diariamente para que otros sistemas tengan a su disposición la información actualizada. Debes crear también una API para consultar los datos, que permita:

- Listar las SICAVs filtradas por fecha de creación, por el número de registro, ISIN y nombre.
- Acceso a todos los datos de una SICAV por su ISIN. Al acceder este endpoint deberá devolver la información actual y un listado de cambios observados y la fecha en que se han observado. El domicilio, capitales y fecha de último folleto pueden cambiar entre extracción y extracción.

El software debe estar escrito en python y los datos persistidos en MongoDB. Con el objetivo de facilitar la evaluación de la prueba es necesario el uso también de Docker y Docker-compose.

## Descripción general del proyecto

El repositorio presenta una solución para la prueba del apartado anterior. Para su realización, se ha adoptado python y persitimos los datos en MongoDB que se ejecuta dentro de un contenedor docker. Respecto a la gestión de dependencias, versionamiento, calidad de código, test unitario y despliegue, tenemos el conjunto de tecnologías descrito en el próximo apartado.

### Gestión de dependencias, versionamiento, code formatting, test unitario y despliegue

- Gestión de dependencias: Utilizamos [poetry](https://python-poetry.org/) que nos permite definir las dependencias de nuestro proyecto estableciendo las relaciones entre paquetes y generando un archivo lock con el correcto versionamiento de las dependencias. Poetry también nos permite crear grupos de dependencias que pueden ser utilizados a distintos niveles durante la instalación, manteniendo su compatibilidad con las demás dependencias del proyecto.  

- Versionamiento: Utilizamos git.

- Code formatting: Para formatear el código utilizando estándares de código a nivel de producción en Python, utilizamos aquí tres herramientas distintas y las configuraciones específicias de cada una de las herramientas se encuentra en el archivo [pyproject.toml](https://github.com/joseilberto/flanks-challenge/blob/main/pyproject.toml):
  - [black](https://black.readthedocs.io/en/stable/): Se utiliza black con sus opciones por defecto y con el tamañno de la línea a 80 caracteres. El código se formatea automáticamente y nos permite mantener la estética del código ordenada en todos los archivos siguiendo el formato de PEP8 por defecto.
  - [pylint](https://www.pylint.org/): Pylint es un linter que hace respetar los estándares del PEP8 para el código, comprueba los imports y su órden en el código y nos permite, detecta posibles errores que se verían durante el runtime, contribuye para la refactoración del código reduciendo el riesgo de adoptar posibles malas prácticas.
  - [mypy](https://mypy-lang.org/): Es un optional static type checker para Python y nos permite comprobar los tipos de variables utilizados, reduciendo el riesgo de que funciones reciban y devuelvan parámetros de distintos tipos.

- Test unitario: En el presente proyecto, testeamos el código del crawler únicamente. La insignia de cobertura en este documento corresponde solamente a la cobertura de las clases y métodos relacionados al crawler, no hay tests unitarios relacionados al servicio. Los tests utilizan [pytest](https://docs.pytest.org/en/7.4.x/) y se ejecutan antes de la ejecución del crawler.

- Despliegue: Adoptamos [Docker](https://www.docker.com/) y [Docker compose](https://docs.docker.com/compose/) para la creación de contenedores que simplifiquen el uso del código y las dependencias que tenemos para el proyecto.

Como descrito en la prueba, se espera que inicialmente generemos tres contenedores Docker para permitir el uso de MongoDB, testear el código del crawler y, por fin, ejecutar el crawler y persistir los datos en MongoDB. De manera opcional, para la ejecución del servicio, he creado un archivo docker compose que crea un contenedor con MongoDB y otro contenedor donde se ejecuta el servicio. Más detalles de las dos estructuras se encuentran en el siguiente apartado.

### Estructura de contenedores
