# coppelPrueba
prueba de microservicios para coppel

## Como correr el proyecto
Tienes que crear en la carpeta raiz una carpeta llamada data.

Despues ejecuta el siguiente comando

### Obtencion de llave privada
en tu terminal linux ejecuta el siguiente comando
```
openssl rand -hex 32
```
esto te recomendara una llave que puedes usar para el proyecto

### Creacion de archivo docker compose

este es un ejemplo de como se deberia de ver el docker compose
```
version: "3.9" 

services:
  mongo:
    image: mongo:latest
    restart: always
    container_name: "mongodb"
    hostname: host-mongo
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: admin
    volumes:
    # del lado izquierdo es nuestra maquina
    # el derecho es lo de contenedor
    # se divide antes y depues de los puntos
      - './data:/data/db'
    ports:
    # la misma logica de los puntos
        - '27017:27017'
  
  rabbitmq3:
    container_name: "rabbitmq3"
    image: rabbitmq:3.8-management-alpine
    hostname: host-rabbit
    environment:
        - RABBITMQ_DEFAULT_USER=guest
        - RABBITMQ_DEFAULT_PASS=guest
    ports:
        # AMQP protocol port
        - '5672:5672'
        # HTTP management UI
        - '15672:15672'

  addcomics:
    build: ./servicios/agregarcomics
    ports:
      - '8008:8008'
    volumes:
      - ./servicios/agregarcomics:/app
    environment:
      - SECRET_KEY=1234

  busquedacomics:
    build: ./servicios/busqueda
    hostname: host-busqueda
    ports:
      - '8005:8005'
    volumes:
      - ./servicios/busqueda:/app
  
  usuarios:
    build: ./servicios/usuarios
    hostname: hostusuarios
    ports:
      - '8000:8000'
    volumes:
      - ./servicios/usuarios:/app
    environment:
      - SECRET_KEY=1234
```

copialo y pegalo de esta forma solo cambia las variables de **SECRET_KEY** por las que generaste.   

Por ultimo ejecuta el siguiente comando

```
docker-compose up
```
