# Renting Room Api

Renting Room Api es una Api Rest que integra la mayoria de los conocimientos que he adquirido hasta el 1 de Noviembre del 2022 como desarrollador de Apis. El siguiente proyecto ha sido contruido con base en los siguientes lenguajes, frameworks, herramientas, patrones de diseño y conceptos

* `Python==3.9` + `Django==4.1` + `django-rest-framework==3.14`
* Django esta basado ORM y la patron de diseño de software VMC
* Hypermedia
* Documentación con `drf-yasg==1.21`
* Dockers y Kubernetes
* Unit Test con `rest_framework`

## 1.- Instalación

crear el archivo de variables del ambiente `.env`, llenar con la data apropiada de su base de datos

### 1.1.- Local

#### Requerimientos:

- python 3.9
- postgres 12+ (database: booking o el nombre escogido en `.env`)

#### Commandos:

```bash
$ python -m venv venv
$ source .\venv\Scripts\activate
(venv) $ pip install -r requirements.txt
(venv) $ python manage.py migrate
(venv) $ python manage.py loaddata booking.json
(venv) $ python manage.py runserver
```

La aplicacion sera accesible desde http://127.0.0.1:8000/

### 1.2.- Dockers

#### Requerimientos:
- docker

```bash
$ docker build .
$ docker-compose run web python manage.py migrate
$ docker-compose run web python manage.py loaddata booking.json
$ docker-compose up
```
La aplicacion sera accesible desde http://127.0.0.1:8090/

## 2.- Elaboración del proyecto

### 2.1.- Definición del sistema

En el sistema se pueden registrar Cuartos, Eventos y Reservaciones para dichos eventos, ademas el sistema cuenta con el registro de usuarios con dos roles: **Consumidores** y **Negociantes**. Para cualquier cliente del sistema, logueado o no, se le referira como **Cliente**.

Reglas del negocio:

Cuartos :
- Los cuartos tiene capacidades distintas.
- Los **Clientes** puede listar los cuartos existentes.
- Solo los **Negociantes** pueden registrar cuartos.
- Los **Clientes** pueden recuperar cualquier cuarto.
- Los cuartos no pueden ser modificados.
- Solo los **Negociantes** pueden borrar un cuarto.
- los cuartos solo pueden ser borrados si no tienen **eventos proximos**.

Eventos:
- Los Eventos tienen fecha y titulo, se realizan en un cuarto y pueden ser privados o publicos.
- Los **Clientes** pueden listar los eventos punlicos.
- Los eventos privados solo se listaran si dicho evento le pertenece al usuario o si el usuario tiene reservacion para dicho evento.
- Solo los **Negociantes** Pueden crear eventos.
- No se pueden crear dos eventos el mismo dia en el mismo cuarto
- Los **Clientes** pueden recuperar cualquier evento publico
- Los eventos privados solo puede ser recuperados por el dueño del evento o si el usuario tiene reservación.
- Solo los dueños de los eventos pueden modificar dicho evento
- actualemnte solo se puede modificar el titulo del evento
- No se puede borrar un evento

Reservaciones:
- Las reservaciones le pertenecen a un usuario y se realizan para un evento
- solo se podran regresar las reservaciones si es dueño de dicha reservacion o dueño del evento
- los **Consumidores** pueden registrarse a ellos mismos, los **Negociantes** pueden resitrar a otros usuarios
- No se puede hacer una reservacion para un usuario en un mismo evento dos veces.
- No se puede hacer una reservacion para un evento si el mosmo esta lleno
- Solo el dueño de una reservacion o del evento al que pertenece puede regresar dicha reservación
- no se puede modificar una reservacion
- solo el dueño de una reservacion o del evento al que pertenece puede borrar dicha reservacion
- al borrar una reservación ese espacio debe estar nuevamente disponible

### 2.2.- Hipermedia

Antes de este proyecto no era conocido el concepto de Hipermedia. Para este proyecto se decidieron agregar las siguientes secuencias

ingresando al sistema se puede acceder a las listas de cuartos, eventos y reservaciones

desde los cuartos se puede acceder a cada cuarto
desde cada cuarto se puede acceder a sus proximos 5 eventos
desde los eventos se puede acceder a cada evento y su respectivo cuarto
desde cada evento, si es dueño, se puede acceder a cada reservacion y su usario
desde las reservaciones se puede acceder a cada reservacion y a su evento
desde cada reservacion se puede acceder a cada evento 

### 2.3.- Documentación

Para la documentación de la api se decidio usar `drf-yasg` con `redocs` por su diseño y la capacidad de ser modificacble. Esta se puede acceder desde `/redocs/`.

### 2.4.- Dockerización

Para este proyecto se tuvo que aprender Dockers. Afortunadamente fue realativamente sencillo su implementación dada su amplia documentación para Django

### 2.5.- Kubernetes

### 2.6.- Servicio SaaS o FaaS