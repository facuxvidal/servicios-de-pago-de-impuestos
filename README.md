# servicios-de-pago-de-impuestos
Simple API de proveedor de servicios de pago de impuestos

## Documentación Web Api
Se puede acceder a los servicios actualmente disponibles de la API mediante `<ip_host>:<puerto_host>/docs`. Dentro cada endpoint se detalla su funcionamiento.
Localmente [localhost:8080/docs](localhost:8080/docs).

## Levantar la API localmente
### Requerimientos
Tener instalado en su maquina:

* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)
* [Git](https://git-scm.com/downloads)

### Instrucciones 
* Clonar el repositorio del proyecto desde [https://github.com/facuxvidal/servicios-de-pago-de-impuestos.git](https://github.com/facuxvidal/servicios-de-pago-de-impuestos.git).
* Iniciar **Docker**.
* Abrir una terminal, situarse sobre la carpeta raiz del proyecto y ejecutar `docker compose up`.
* Entrar a [localhost:8080/docs](localhost:8080/docs) para ver y probar los servicios disponibles.