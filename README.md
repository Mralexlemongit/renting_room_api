# Renting Room Api

Renting Room es una Api Rest que integra la mayoría de los conocimientos que he adquirido hasta el 1 de noviembre del 2022 como desarrollador de Apis. El siguiente proyecto ha sido construido con base en los siguientes lenguajes, frameworks, herramientas, patrones de diseño y conceptos.

* `Python==3.9` + `Django==4.1` + `django-rest-framework==3.14` (VMC, ORM, Api Rest).
* Hypermedia.
* Documentación con `drf-yasg==1.21`.
* Dockers y Kubernetes.
* Unit Test con `rest_framework`.

## 1. Instalación

crear el archivo `.env` basado en `.env_template`.

### 1.1. Local

#### Requerimientos:

- Python 3.9.
- Postgres 13 (opcional).

Opcional: Si se desea ejecutar el proyecto con sqllite (o no se tiene instalado Postgres) cambiar la variable `USING_POSTGRES_DATABASE` a `False`. 

#### Comandos:

```bash
$ python -m venv venv
$ source .\venv\Scripts\activate
(venv) $ cd project
(venv) $ pip install -r requirements.txt
(venv) $ python manage.py migrate
(venv) $ python manage.py loaddata booking.json
(venv) $ python manage.py runserver
```

La aplicación será accesible desde http://127.0.0.1:8000/

### 1.2. Dockers

#### Requerimientos:
- Docker.

#### Comandos:

```bash
$ docker build .
$ docker-compose run web python manage.py migrate
$ docker-compose run web python manage.py loaddata booking.json
$ docker-compose up
```
La aplicación será accesible desde http://127.0.0.1:8090/

## 2. Elaboración del proyecto

### 2.1. Definición del sistema

En el sistema se pueden registrar Cuartos, Eventos y crear Reservaciones para dichos eventos, además el sistema cuenta con el registro de usuarios con dos roles: **Consumidores** y **Negociantes**. A cualquier cliente del sistema, registrado o no, se le referirá como **Cliente**. A cualquier cliente del sistema registrado se le referirá como **Usuario**.

Reglas del negocio:

Cuartos:
- Los cuartos tienen capacidades distintas.
- Los **Clientes** puede listar los cuartos existentes.
- Solo los **Negociantes** pueden registrar cuartos.
- Los **Clientes** pueden recuperar cualquier cuarto.
- Los cuartos no pueden ser modificados.
- Solo los **Negociantes** pueden borrar un cuarto.
- Los cuartos solo pueden ser borrados si no tienen **eventos próximos**.

Eventos:
- Los Eventos tienen fecha y título, se realizan en un cuarto y pueden ser privados o públicos.
- Los **Clientes** pueden listar los eventos públicos.
- Un **Usuario** puede ver todos los eventos públicos más los eventos privados en los que tenga reservación.
- Solo los **Negociantes** Pueden crear eventos.
- No se pueden crear dos eventos el mismo día en el mismo cuarto.
- Los **Clientes** pueden recuperar cualquier evento público.
- Los eventos privados solo puede ser recuperados por el **Dueño del evento** o si el **Usuario** tiene reservación.
- Solo los **Dueños de los eventos** pueden modificar dicho evento.
- Actualmente, solo se puede modificar el título del evento.
- No se puede borrar un evento.

Reservaciones:
- Las reservaciones le pertenecen a un **Usuario** y se realizan para un evento.
- Cualquier **Usuario** puede listar las reservaciones.
- Solo visibles las reservaciones si se es dueño de dicha reservación o dueño del evento al que la reservación pertenece.
- Los **Consumidores** pueden registrarse a ellos mismos, los **Negociantes** pueden registrar a otros **Usuarios**.
- No se puede hacer una reservación para un **Usuario** en un mismo evento dos veces.
- No se puede hacer una reservación para un evento si el mismo está lleno.
- Solo el **dueño de una reservación o del evento al que pertenece** puede regresar dicha reservación.
- No se puede modificar una reservación.
- Solo el **dueño de una reservación o del evento al que pertenece** puede borrar dicha reservación.
- Al borrar una reservación, ese espacio debe estar nuevamente disponible.

### 2.2. Hipermedia

Antes de este proyecto no era conocido el concepto de Hipermedia. Para este proyecto se decidieron agregar las siguientes secuencias

- Ingresando al sistema se puede acceder a las listas de cuartos, eventos y reservaciones.
- Desde los cuartos se puede acceder a cada cuarto.
- Desde cada cuarto se puede acceder a sus próximos 5 eventos.
- Desde los eventos se puede acceder a cada evento y su respectivo cuarto.
- Desde cada evento, si es dueño, se puede acceder a cada reservación y su usuario.
- Desde las reservaciones se puede acceder a cada reservación y a su evento.
- Desde cada reservación se puede acceder a cada evento.

### 2.3. Documentación

Para la documentación de la api se decidió usar `drf-yasg` con `redocs` por su diseño y la capacidad de ser modificable. Esta se puede acceder desde `/redocs/`.

### 2.4. Dockerización

Para este proyecto se tuvo que aprender Dockers. Afortunadamente, fue relativamente sencillo su implementación dada su amplia documentación para Django. Se tuvo que instalar Docker y el complemento WSL2. Hubo dos problemas grandes en esta tarea, el primero fue entender cuáles eran los comandos mínimos para poder levantar el ambiente. El segundo sucede de la decisión del movimiento de carpetas para limpieza de la estructura del código, esto termino en una reestructuración de los archivos `Dockerfile` y `docker-compose.yml` y lograr una comprensión sencilla de sus comandos.

### 2.5. Kubernetes y Servicio SaaS o FaaS

Para kubernetes se descargaron e instalaron los binarios de `Minikube` y `Kubectl`, siguiendo una guía nos quedamos atorados en el siguiente paso

```cmd
$ minikube start --vm-driver=virtualbox

minikube v1.8.2 on Microsoft Windows 10 Enterprise 10.0.18363 Build 18363
Using the hyperv driver based on existing profile
Reconfiguring existing host ...
Using the running hyperv "minikube" VM ...
! Node may be unable to resolve external DNS records
! VM is unable to access k8s.gcr.io, you may need to configure a proxy or set --image-repository
```

Siguiendo los pasos se pudo levantar minikube, pero se me mostraban `0/2` en los pods donde se esperaban `2/2` y al acceder a la ruta que entregaban los comandos `x.x.x.x:yyyy` no mostraba nada.

Al no encontrar suficiente información al respecto de como arreglar el problema y con carencia de tiempo, decidí enfocarme en pulir la aplicación principal.

### 2.6. Tests

Local:

```bash
(venv) $ python manage.py test
```

Dockers:


```bash
$ docker-compose run web python manage.py test
```