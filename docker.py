"""
Los tres grandes problemas del desarrollow de software.

- Construir | Como construimos el software.
- Distribuir | Como hacemos que llegue el software a donde tiene que llegar.
- Ejecutar | Como haceos que corra como tiene que correr.

!Construir:

- Entorno de desarrollo.
Uno tiene su maquina, con sus versiones de sus herramientas, del codigo.

- Dependencias.
Esto tmb es un problema ya que usamos mucho esto y pueden ser distintas con otros equipos de trabajo

- Entorno de ejecución.
Por ejemplo si estamos corriendo node, y las versiones son distintas, trae problemas.

- Equivalencia con entorno productivo.
Que sea lo más parecido o adecuado a donde se apunta el producto, si se programa y prueba el software para os linux en windows es 
un problema

- Servicios Exrternos.
Si nuestro software va a usar dbs, que db, que version, compatibilidad, etc.


!Distribuir Software:

- Divergencia de repositorios

- Divergencia de artefactos

- Versionado

!Ejecutar Software

- Compatibilidad con el entorno productivo

- Dependencias

- Disponibilidad de servicios externos

- Recursos de hardware

------------------------------------------------------------------------------------

"Docker permite construir distribuir y ejecutar cualquier app en cualquier lado"

------------------------------------------------------------------------------------

VIRTUALIZACIÓN

Es la version virtual de algún recurso tecnologico (hardware, os, dispositivo de almacenamiento, recurso de red, etc)
Esto es lo que nos va a permitir atacar los 3 problemas del software.

CONTENEDORES 

El empleo de contenedores para construir y desplegar software....
Estos son

-Flexibles ----> Se puede meter cualquier aplicación

-Livianos ----> Al utilizar el kernel del os que los contiene, no tiene el problema de las vm que lo que hacen es tener otra vez toda la 
configuracion del sistema

-Portables ---> Se van a ejecutar de la misma manera en cualquier maquina

-Bajo acoplamiento ---> Con el sistema que lo corre, ya que son autocontenidos (tiene todo lo necesario para correr)

-Escalables ----> Es facil crear contenedores para ampliar el ancho de banda, etc. Por lo que es escalable.

-Seguros 

---------------------------------

?$ docker --version

?$ docker info 
Para ver informacion de la instalacion de docker.

¿ Que es y que hace ?
    
Client docker CLI (Command Line Interface)
        |
        V
Corazon de docker ----> docker daemon (maneja las identidades)

"""
Identidads = {
    "Contenedores": "Alojan tecnologias y las aplicaciones.",
    "Imagenes": "Artefactos que usa docker para empaquetar contenedores",
    "DataVolumes": "Forma en la que docker permite acceder al sistema de archivos de la maquina anfritiona",
    "Network": "Permite a los distintos contenedores comunicarse entre si o con el mundo exterior"
}
"""
    CONTAINER ID            IMAGE           COMMAND             CREATED             STATUS    PORTS     NAMES
    id del container       imagenes    Proceso que corre     fecha de creacion      Estado    Puertos    Nombre
                                          al arrancar

Por ejemplo, podriamos crear un container de linux, super simple con docker 

?$ docker run ubuntu

De esta manera  creamos y ejecutamos un contenedor de linux, pero vemos que no hace nada, vemos que el status es Exited(0) y el command
es /bin/bash, lo que indica que esto se ejecuto correctamente, pero como no tiene nada para hacer, se termino con un estado exitoso (0)

?$ docker run -it ubuntu
-i  Modo interactivo
-t  Abrir la consola

!CICLO DE VIDA DE UN CONTENEDOR

Cada vez que un contenedor se ejecuta, en realidad ejecuta un proceso del sistema operativo. Este mismo es el que determina si el contenedor
sigue vivo o no. El contenedor va a estar vivo y ejecutandose siempre y cuando el commando que corre la iniciar este corriendo de manera 
exitosa.

?$ docker run --name test (-d || --detach) ubuntu tail -f /dev/null
Lo que hace es crear y correr un contenedor de nombre test con ubunto pero el parametro -d lo que hace es correrlo en segundo plano, es 
decir, iniciara de la misma manera que siempre pero se va a separar del contenedor, y a su vez, luego del contenedor (ubuntu) iria el 
commando inicial que quiero que corra al iniciar, en este caso (tail -f /dev/null, es un comando sin fin)

Esto va a devolver un id, el id del proceso.

?$ docker exec 
Lo que permite es, en un container que ya esta corriendo, ejecutar un comando o proceso.

Por lo tanto podria ejecutar

?$ docker exec -it test bash
Ejecutar en la bash de manera interactiva el comando bash en el container test

Esto nos arrojaria una consola interactiva de manera que si tiraramos el comando ps -aux, podriamos ver todos los comandos que se estan 
ejecutando y veriamos vivo nuestro comando inicial de tail -f /dev/null, por lo tanto, esto nos puede ayudar a entender que si, nosotros
tiramos exit, matando el proceso nuevo creado de la bash, tail -f /dev/null seguiria corriendo, y mientras no muera el proceso inicial de 
un contenedor, el mismo no va a morir.

Por lo tanto hay que entender, que el comando tail -f /dev/null es un proceso que se esta corriendo de manera nativa en nuestro sistema
operativo, por lo que si lo qusiera matar, podria utilizar el comando 

?$ docker inspect --format '{{.State.Pid}}' test
Recordemos que 'docker inspect {name/id}' devuelve un json enorme de informacion del container, con el '--format' lo que hacemos es aplicar
un filtrado por la string '{{.State.Pid}}' en el cual va a estar alojado el pid del proceso que se esta corriendo

----------------------------------------------------------------------------------------------------------------

Ejemplo practico hecho en mi sistema:

❯ docker inspect --format '{{.State.Pid}}' linux_test
3528426

❯ ps -aux | grep "3528426"
root     3528426  0.0  0.0   2820  1008 ?        Ss   12:11   0:00 tail -f /dev/null

❯ sudo kill -9 3528426

❯ ps -aux | grep "3528426"

----------------------------------------------------------------------------------------------------------------

?$ docker run -d --name proxy nginx 
Nginx es un servidor web que también se puede utilizar como proxy inverso, equilibrador de carga, proxy de correo y caché HTTP.

Al ejecutar este contenedor vamos a ver algo nuevo, y es que, si hacemos docker ps veremos la parte del puerto con algo como 80/tcp

CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS     NAMES
c09ce1944a77   nginx     "/docker-entrypoint.…"   44 seconds ago   Up 29 seconds   80/tcp    proxy

Cada contenedor tiene su propia interfaz de red, por lo que el contenedor esta escuchand en el puerto 80 del contenedor, pero no es el 
puerto 80 de nuestro sistema operativo. Por lo que si fueramos al puerto 80 no veriamos nada, por lo que tenemos que hacer es especificar
que el puerto 80 de ese contenedor apunte a un puerto de nuestro sistema.

De esta manera, con el nuevo arg, -p de (PUBLISH / PORT) ingresamos separados por : de la izquiera nuestro puerto a exponer y conectar con
el puerto del contenedor yendo este del lado derecho de los :

Por lo que seria

?$ docker run -d --name proxy -p 8080:80 nginx
De esta manera, estamos diciendo que levante y cree un nuevo container de nombre proxy, que lo independice y que en el puerto 8080 de nuestra
maquina se conecte con el puerto 80 del contenedor 

Por lo que si hicieramos docker ps

PORTS               
0.0.0.0:8080->80/tcp

Para ver los logs de un contenedor, 

?$ docker logs {docker_name/id}

?$ docker logs -f {docker_name/id}
-f ---> follow, no dejar de ver los logs

!MANEJO DE DATOS EN DOCKER | Bind Mounts

En que consiste esto? Por ejemplo, si crearamos un contenedor con la imagen de mongo, creariamos nuestra base de datos, insertariamos datos 
y todo estaria bien, el problema seria que a la hora de eliminar este, todos los datos se perderian de manera que no se podria recuperar.
Como se podrian manejar los datos de manera que si borrase el contenedor y levantara otro los datos fueran compartidos? Con Bind Mounts

?$ docker run -d --name db -v /path/:/container/path mongo 

----------------------------------------------------------------------------------------------------------------

Ejemplo practico:

?$ docker run -d --name -v /home/user/Desktop/docker/mongotest:/data/db mongo

Docker guarda la informacion en la carpeta /data/db por lo que estamos haciendo es una especie de "enlace simbolico" a nuestra ruta
/home/user/Desktop/docker/mongotest

Por lo que si ahora con el contenedor db creado realizamos los sig

?$ docker exec -it db bash
Ejecutamos una bash con una terminal intercatiba para el contenedor db

?$ mongosh
Abrimos el gestor de base de datos de mongo

?$ show dbs
Para ver las base de datos

?$ use usuarios
Para crear una base de datos (USUARIOS)

?$ db.users.insertOne({"name":"Dobliuw"})
En la base de datos que creamos previamente y estamos usando (usuarios) creamos la tabla "users" y le insertamos 
el dato del obj {"name":"Dobliuw"}

De esta manera creamos una base de datos "usuarios" con la tabla "users" que tiene un campo "{"name":"Dobliuw"}"

Por lo que si ahora borramos este contenedor y creamos otro, realizamos el mismo proceso y ejecutamos el sig comando antes de insertar 
datos en la tabla: 

?$ db.users.find()

Veriamos al obj {"name":"Dobliuw"} y tambien en el directorio especificado (en nuestro ejemplo /home/user/Desktop/docker/mongotest), veriamos
muchas carpetas:

 diagnostic.data                        collection-2--8411566656645472637.wt  
 index-3--8411566656645472637.wt        mongod.lock                                WiredTiger.lock
 journal                                collection-4--8411566656645472637.wt  
 index-5--8411566656645472637.wt        sizeStorer.wt                              WiredTiger.turtle
 _mdb_catalog.wt                        collection-7--8411566656645472637.wt  
 index-6--8411566656645472637.wt        storage.bson                               WiredTiger.wt
 collection-0--8411566656645472637.wt   index-1--8411566656645472637.wt       
 index-8--8411566656645472637.wt        WiredTiger                                 WiredTigerHS.wt


*ADICIONAL DE REGALO

Este mismo concepto, se puede utilizar para la escalación de privilegios, al ingresar al sistema, podriamos ver si nuestro usuario target
se encuentra en el grupo docker

?$ id 

En caso de que contenga el grupo docker, podriamos ver si posee alguna imagen descargada o creada

?$ docker images

En caso de contener alguna imagen, podriamos aprovecharnos de la misma, para ejecutar un contenedor y haciendo uso de los Bind mounts, 
buildar el contenedor con la raiz del sistema operativo a escalar en la ruta /mnt/root

?$ docker run -dit --name privilegeEscalation -v /:/mnt/root {nombre_de_la_imagen_encontrada}

De esta manera estariamos creando un contenedor de nombre privilegeEscalation poniendolo en segundo plano con una bash interactiva 
permitiendonos acceder en el directorio /mnt/root el acceso a todo el sistema operativo.

Puediendo de esta manera ejecutar una bash y estando como usuario root o incluso puediendo asignar permisos suid a la bash, para de una 
manera más comoda poder ejecutar comandos.

?$ chmod +s /bin/bash

----------------------------------------------------------------------------------------------------------------

!Volúmenes

Debido a que con bindmounts podemos tener problemas de seguridad, docker creo una manera más segura de guardar los datos que son los 
volúmenes, son unidades de almacenamiento designadas y administradas por docker, de esta manera tenemos los datos de una manera sentralizada
que los usuarios no pueden ver

?$ docker volume ls 
Listamos los volumenes existentes

?$ docker volume create {volume_name}
Creamos un volumen

?$ docker run -d --name {container_name} --mount src={volume_name},dst={container_path} {image_name}
Creamos y ejecutamos un container con una imagen dada, poniendolo en segundo plano con detach, con el nombre indicado donde lo 
montamos (--mount) en una destino (source --> src ) y le hacemos referencia al path del contenedor (destino ---> dst)

De esta manera igual que con las binds mount, todo lo que el contenedor deposite en la ruta {container_path} se estara alojando en el
volumen creado {container_name}

?$ docker inspect {image_name} | grep -A 4 "Mounts" 
Recordemos que podriamos ver la informacion del contenedor con inspect y podriamos filtrar por la palabra Mounts exentiendolo 4 lineas hacia
abajo para ver asi datos de en que volumen se encuentra, en que path se encuentra el volumne, etc.

!Insertar y extraear archivos de un contenedor 

Hasta el momento entendemos que con los bind mounts alojamos ciertos datos que querramos del contenedor en una ruta de nuestro sistema
Con Volumenes pasa lo mismo pero es en un area de directorios reinstringidos que controla docker siendo esto más seguro y practico

Ahora, usando Bind mounts o volumnes o ninguno, podemos ingresar y sacar archivos del contenedor, esto lo podemos hacer de una manera muy
sensilla sin importar si el container esta o no apagado.

?$ docker cp {file} {destination}

Example:

?$ docker cp example.txt containerTest:/test
Copiame el archivo example.txt a la ruta /test del container llamado "containerTest" 

?$ docker cp containerTest:/test example2.txt 
Copiame desde la ruta /test del container llamado "containerTest" el archivo example2.txt

-------

tmpfs ---> Temporaly file system mount 

Esto esa solo para linux, es una porcion de disco que solo existe en memoria que no nos interesan perder al morir el contenedor. No tiene
persistencia en disco

-------

!IMAGENES

Las imagenes son "Moldes" a partir de las que docker genera contenedores, son piezas de software livianas. Todo lo que el contenedor necesita
par que se ejecute.

?$ docker image ls 

REPOSITORY                   TAG                           IMAGE ID       CREATED          SIZE
repo           Version(si no especificamos, latest)           id        cuando se creo     peso

Las imagenes en el disco viven como un conjunto de archivos o capas, es un conjunto de archivos que forman la imagen. De esta manera
es como gana eficiencia transmitiendo estas entre sistemas. Estas se descargan desde "Docker Hub"

?$ docker pull ubuntu:20.04
Esto es para descargar del repositorio de Docker Hub la imagen de ubuntu version 20.04

Si tuvieramos la imagen de ubuntu version latest y la 20.04 en la pagina de DockerHub tendria este mismo tag, veriamos que al hacer 
"docker image ls" tendriamos dos imagenes de ubuntu, con  el tag diferente pero todo lo demas igual, y esto no quiere decir que tengamos
dos imagenes iguales, simplemente que tenemos dos "punteros" que indican a una misma imagen.

Ejemplo practico:

ubuntu        22.04     6b7dfa7e8fdb   5 weeks ago     77.8MB
ubuntu        latest    6b7dfa7e8fdb   5 weeks ago     77.8MB

!COMO CREAR NUESTRA PROPIA IMAGEN?

Esta proceso siempre va a estar basado en un archivo (dockerFile) 

?$ nano Dockerfile

Las imagenes siempre van a estar basadas en otra imagen, por lo tanto la primera linea siempre va a ser 

FROM {image:version}

?$-------------------------------------------------------------------------------
?$      FROM ubuntu:latest
?$
?$      RUN touch /usr/src/myFisrstImage.txt 
?$-----------------------------------------------------------------------------
 
Por ejemplo aca estariamos creando nuestra primera imagen, la cual parte de ubuntu y se encarga de crear un archivo .txt en la ruta 
/usr/src

Una vez escrito el DockerFile solo queda crear la imagen.

?$ docker build -t {image_name}:{image_version} --file {docker_file} {path_to_create}

?$ docker build -t ubuntu:dobliuw --file ./Dockerfile . 
Esto buildearia la imagen con las instrucciones del Dockerfile y la llamaria ubuntu version "dobliuw"

?$ docker image ls 

REPOSITORY    TAG       IMAGE ID       CREATED              SIZE
ubuntu        dobliuw   f5c58ce9fd93   About a minute ago   77.8MB

De esta manera ahora podriamos crear y levantar nuestro contenedor basado en nuestra imagen la cual va a ejecutar lo que le hayamos indicado
Por lo que si ejecutamos:

?$ docker run -dit --name ubu ubuntu:dobliuw tail -f /dev/null 

?$ docker exec -it ubu sh 

Tendriamos un container levantado con el nombre de ubu basado en nuestra imagen ubuntu:dobliuw y posteriormente nos lanzariamos una shell 
de manera interactiva para ver que en la ruta /usr/src se econtrara el archivo myFirstImage.txt 

IMPORTANTE: Todo lo que se ejecuta en el DockerFile, se hace en tiempo de build.

Una vez que tenemos nuestra imagen, la podemos subir al repo de Docker Hub, pero previamente hay que loguearse 

?$ docker login -u {user}
Password o token

?$ docker tag {prev_name_image} {new_name_image}
?$ docker tag ubuntu:script dobliuw/ubuntu:script
manera convencional de llamar una imagen, name/dist:version

?$ docker push dobliuw/ubuntu:script

!SISTEMA DE CAPAS

Lo bueno de las imagenes, es que podemos ver mediante el docker file, como esta construida la misma

?$ docker history {image_name}
Comando para ver las capas de la imagen

!ENTORNO PROFESIONAL

Ahora... como usamos todo esto? Un buen ejemplo es el repo ---> https://github.com/platzi/docker

?$ docker build -t platziapp --file ./Dockerfile . 

?$ docker run --rm --name node -p 80:3000 platziapp

para con el docker file --> 

--------------------------------------------

FROM node:12

COPY [".", "/usr/src/"]

WORKDIR /usr/src

RUN npm install

EXPOSE 3000

CMD ["node", "index.js"]

--------------------------------------------

!APROVECHANDO EL CACHE DE LAS CAPAS PARA IMAGENES

Basandonos en el Docker file anterior

--------------------------------------------

FROM node:12

COPY ["package.json", "package-lock.json", "/usr/src/"]

WORKDIR /usr/src

RUN npm install

COPY [".", "/usr/src/"]

EXPOSE 3000

CMD ["node", "index.js"]

--------------------------------------------

De esta manera no sera necesario re instalar nodejs una y otra vez.
Incluso por ejemplo podriamos utilizar nodemon

CMD ["npx", "nodemon", index.js"] <-----

permitiendo de esta manera realizar cambios sin tener que rebuildear la image.

?$ docker run --rm --name node -v /path/index.js:/usr/src/index.js platziapp

!CONEXIONES ENTRE CONTENEDORES (Docker networking)

?$ docker network ls 
Listar conexiones de las redes

host ---> red real de mi pc
none ---> red especial, lo podemos usar si queremos que un contenedor no tenga red

Para crear nuestra red

?$ docker network create dobliuwnet
Pero ademas de crearla, quiero que otros contenedores se conecten "--attachable" 

?$ docker network create --attachable dobliuwnet

?$ docker network inspect dobliuwnet

?$ docker network connect {network} {container}

De es manera, podriamos tener un contenedor como el previamente creado, con la sig imagen:

--------------------------------------------------------

FROM node:12

COPY ["package.json", "package-lock.json", "/usr/src/"]

WORKDIR /usr/src

RUN npm install

COPY [".", "/usr/src/"]

EXPOSE 3000

CMD ["node", "index.js"]

--------------------------------------------------------

Por lo que podriamos levantarlo, tomando como ejemplo que la imagen de arriba se llama "dobliuwapp" y el codigo que existe contiene una
conexion a una db de mongo con una variable de entorno llamada MONGO_URL 

----------------------------------------------------------------------------------------------------------------
       │ File: index.js
───────┼───────────────────────────────────────────────────────────────────────────────────────
   1   │ const express = require('express')
   2   │ const app = express()
   3   │ const port = 3000
   4   │ 
   5   │ const MongoClient = require('mongodb').MongoClient
   6   │ 
   7   │ // Connection URL
   8   │ const mongoUrl = process.env.MONGO_URL || 'mongodb://localhost:27017/test';
   9   │ 
  10   │ app.get('/', (req, res) => {
  11   │   MongoClient.connect(mongoUrl, { useNewUrlParser: true }, (err, db) => {
  12   │     if (err) {
  13 ~ │       res.status(500).send('---> BOOM <--- : ' + err);
  14   │     } else {
  15   │       res.send('Me conecté a la DB! 😎');
  16   │       db.close();
  17   │     }
  18   │   });
  19   │ });
  20   │ 
  21   │ app.listen(port, () => console.log(`Server listening on port ${port}!`))
----------------------------------------------------------------------------------------------------------------

Como vemos existe la variable de entorno MONGO_URL, y en mongo, los containers se pueden conectar entre si estando en una misma red, por 
lo que vamos a crear una red

?$ docker network create --attachable dobliuwnet

Una vez creada la red dobliuwnet con el arg --attachable para que otros contenedores se puedan conectar, abria que conectar nuestro primer 
contenedor (la db)

?$ docker run -d --name db mongo 

Una vez creado, lo conectamos a la red

?$ docker network connect dobliuwnet db 

Ahora si, solo quedaria crear nuestro contenedor que contiene el servidor node, con la var de entorno. Como dijimos los contenedores se 
pueden conectar entre si estando en una misma red basandose por el nombre, por lo tanto si ejecutamos

?$ docker network inspect dobliuw net 

Veriamos algo similar a lo sig:

----------------------------------------------------------------------------------------------------------------

[
    {
        "Name": "dobliuwnet",
        "Id": "e0efbfeef75586321fe5877777ad1f82c7c192f27d3f791373d2cdbc2d3bd9c9",
        "Created": "2023-01-18T20:38:05.136182824-03:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": true,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "12613c121122494b8b8f828c7af4c012f9ca3799812668cee988ae00c33083d6": {
                "Name": "node",
                "EndpointID": "0aa2568ffc07530ee2e5542aea372bdb6e7f849dd31a7835ed108f0a29f4ec04",
                "MacAddress": "02:42:ac:12:00:03",
                "IPv4Address": "172.18.0.3/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
]

----------------------------------------------------------------------------------------------------------------

Donde podemos ver una propiedad llamada "Containers" que contiene los containers conectados, y en el "Name" el nombre 
al cual debemos referirnos. Tambien sabemos que el puerto default por el que corre docker es el 27017 
(tmb podemos ver el port de db con docker ps)

Por lo que nuestra variable de entorno podria tener el sig valor:

mongodb://{container_name}:{port}/{path}

mongodb://db:27017/test

mongodb:// es por mongo.

Ahora podriamos pasarle nuestra variable de entorno al contenedor a la hora de crearlo

?$ docker run -d --name node -p 80:3000 --env MONGO_URL=mongodb://db:27017/test dobliuwapp

Ahora solo faltaria conectar los contenedores a la misma red y estaria todo funcional 

?$ docker network connect dobliuwnet node 

Y si hicieramos un 

?$ docker network inspect dobliuwnet 

el apartado de conectores, se veria de la sig manera.

----------------------------------------------------------------------------------------------------------------

 "Containers": {
            "12613c121122494b8b8f828c7af4c012f9ca3799812668cee988ae00c33083d6": {
                "Name": "node",
                "EndpointID": "0aa2568ffc07530ee2e5542aea372bdb6e7f849dd31a7835ed108f0a29f4ec04",
                "MacAddress": "02:42:ac:12:00:03",
                "IPv4Address": "172.18.0.3/16",
                "IPv6Address": ""
            },
            "a38c783f5d9d8be03607ef39661a3826b74b6cc65020290557b6ac8475fb4def": {
                "Name": "db",
                "EndpointID": "11d63b0ace899afecdc87840ec29697467e8baf998fb3d862bef0fe03fb85937",
                "MacAddress": "02:42:ac:12:00:02",
                "IPv4Address": "172.18.0.2/16",
                "IPv6Address": ""
            }
        },

----------------------------------------------------------------------------------------------------------------

!Docker Compose 

22


"""     

"""
Docker Cheat-Sheat

?$ docker --version
Versión de docker.

?$ docker info 
Información de la instalación de docker.

?$ docker run ""
Este comando CREA y EJECUTA un contenedor.

?$ docker ps 
Listar los contenedores desplegados corriendo en el sistema.

?$  docker ps -a 
Listar TODOS los contenedores, corriendo, terminados, etc.

?$ docker inspect {container_ID}
Esto es para ver la configuración de el contenedor.

?$ docker run --name {docker_name} ""
Esto sirve para crear y ejecutar un contenedor pero ingresandole manualmente el nombre. 

?$ docker rename {prev_name} {new_name}
Esto sirve para renombrar un contenedor.

?$ docker rm {container_id/name}
Eliminar un contenedor.

?$ docker container prune 
Eliminar todos los contenedores apagados.

?$ docker rm $(docker ps -a -q) --force
Esto lo que hace es un remove forzado de todos los ids de todos los contenedores globales.

?$ docker exec 
En un container que ya esta corriendo, ejecutar un comando o proceso 

?$ docker run --name {container_name} -p {as_port}:{docker_port} -d nginx
Corremos un container de nginx con un nombre especifico, detachandolo (2do plano) exponiendolo en un puerto especifico y conectandolo
con un puerto del container.

?$ docker logs {docker_name/id}
Esto sirve para ver los logs de un container

?$ docker logs --tail 10 -f {docker_name/id}
Estor sirve para ver en timepo real los logs a medida que lleguen (-f | follow) pero mostrando solo los ultimos 10 (--tail 10)

?$ docker run -dit --name {name} -v /native_operativeSystem/path/:/container/path {image_name}
Esto sirve para hacer un detach (segundo plano) y en una i (interactive) t (terminal/bash) ejecutar nuestro container con la imagen ingresada
llamando a este de la manera ingresada pero dandole acceso a la ruta /native_operativeSystem/path/ en la ruta del contenedor /container/path

?$ docker volume ls 
Listar volumenes

Cabe aclarar que cualquier comando que queramos saber que otras opciones tiene lo podemos ejecutar con --help, ejemplo

?$ docker --help
?$ docker image --help
?$ docker volume --help

?$ docker cp {file} {container}:{path} 
Esto sirve para copiar un archivo a una ruta de un contenedor especifico 

?$ docker cp {container}:{file} {path}
Esto sirve para copiar un archivo de una ruta de un contenedor especifico a un lugar que nosotros querramos  

?$ docker pull {image_name}:{image_version}
Traer del repositorio de Docker Hub una imagen con una version especifica

?$ docker build -t {image_name}:{image_version} --file ./Dockerfile . 
Buildear una imagen con el nombre (-t | TAG ) "{image_name}:{image_version}" partiendo del archivo ./Dockerfile, a partir de este dir.

?$ docker login -u {username}
Logearse en docker

?$ docker push {image_name}:{image_version}
Pushear al repositorio de docker hub la imagen. (tener en cuenta que siempre es {username}/{image_name}:{image_version}) por lo que 
podriamos necesitar renombrar una imagen

?$ docker rename {old_name} {new_name}
Renombra una imagen por un nuevo nombre

?$ docker history {image}
Muestra las capas de la imagen

Tambien para ver de una manera más descriptiva como funciona una imagen, existe la herramienta "dive" 

https://github.com/wagoodman/dive

La cual se ejecuta con 

?$ dive {image_name}

Y entramos en una interfaz en donde con las flechas del taclado podemos ver las capas, asi cmo de la derecha el three del sistema, con 
tab nos podemos ir a este y con ctrl + u dejar solo los archivos modificados, para asi con tab nuevamente volver a las capas y ver capa 
a capa los cambios que se van dando 


-----------------------------------------------------

CREAR DOCKERFILE

FROM ---> IMAGEN DE LA QUE PARTE LA FUTURA NUEVA IMAGEN
RUN ---> EJECUTAR
ADD
COPY [".", "/usr/src"]---> Copiar todo lo de la carpeta actual a /usr/src
CMD ["node", "index.js"] ---> Comando default a ejecutarse en caso de que no ingresemos uno nosotros
WORKDIR /usr/src ----> Es como hacer cd /usr/src
EXPOSE 3000 ---> Que se pueda acceder al contenedor en el puerto 3000

"""
