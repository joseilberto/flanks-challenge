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
