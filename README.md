# Taller de Redes y Servicios
> Conexión entre cliente y servidor mediante contenedores de Docker.


## General Information
- En estas tareas se utilizará la conexión entre el servidor denominado Miniircd, que en este caso ocupará el protocolo IRC (Internet Relay Chat), y el cliente, la cual se utilizará el cliente IRSSI para establecer la conexión con el servidor.
- Luego de establecer la conexión se planea capturar el tráfico que sucede entre éstos.


<!-- You don't have to answer all the questions - just the ones relevant to your project. -->


## Technologies Used
- Terminal Ubuntu 22.04
- Cliente IRSSI  y sus comandos para comunicarse en el servidor IRC.
- Python-3 o superior, con sus dependencias.
- Herramienta Scapy y todas sus librerías
- Herramientas de métricas de red (Netem).


## Setup
Antes de establecer la conexión entre los contenedores del servidor y cliente, se crean los contenedores, ambos con imagen Ubuntu:latest, esto debido a que dentro del servidor se instalarán las herramientas necesarias para la comunicación:

Para el contenedor del servidor:
```diff
sudo docker run -it --name servidor2-container -d ubuntu:latest
```
Se ingresa al contenedor:
```diff
sudo docker exec -it servidor2-container bash
```
Luego dentro de este contenedor:
```diff
# apt-get update
# apt install git
```
Después se clona el repositorio donde se encuentra el servidor Miniircd:
```diff
# git clone https://github.com/jrosdahl/miniircd.git
# cd miniircd
# apt install python3-pip
# pip install mypy
# pip install flake8
# apt install python3-nose
# make
```
Y con esto el servidor ya está instalado en el contenedor y listo para correr.

Y para el contenedor del cliente:
```diff
sudo docker run -it --name cliente-container -d ubuntu:latest
sudo docker exec -it cliente-container bash
```
Dentro del contenedor:
```diff
# apt-get update
# apt install git
```
Con esto se clona el repositorio del cliente:
```diff
# git clone https://github.com/irssi/irssi
cd irssi
meson Build
ninja -C Build && sudo ninja -C Build install
```
Si existen errores, consultar con el repositorio original: https://github.com/irssi/irssi

Finalmente se ejecuta el cliente:
```diff
# irrsi
```

Además para la tarea 3, se crea un contenedor que contendrá Scapy, pero este contenedor tendrá la misma dirección que el servidor, para así traficar y capturar de manera más eficaz:
```diff
sudo docker run -it --name scapy-container ubuntu:latest /bin/bash
```
Adentro de la consola del contenedor, se hará lo siguiente:
```diff
# apt-get update
# apt-get install -y python3 python3-pip libpcap0.8
# pip install scapy
```
Luego se procede a salir del contenedor y se utiliza el comando de Docker "Commit":
```diff
# exit
sudo docker commit scapy-container scapy_image
```
Luego se corre un contenedor con la imagen del Commit:
```diff
docker run -it --name scapy --network container:servidor2-container scapy-image /bin/bash
```

## Usage

Para iniciar el servidor IRC se utiliza el comando:
```diff
# ./miniircd --listen <ip> --setuid <user>
```

Para conectar el cliente con el servidor, en la consola de IRSSI, colocar:
```diff
/connect <ip_server_listening>
```
Para correr los scripts de Python dentro del contenedor de Scapy, simplemente se utiliza: 

```diff
# python3 <script.py>
```

## Acknowledgements

- El proyecto se basó en los repositorios de Miniircd: https://github.com/jrosdahl/miniircd y de IRSSI: https://github.com/irssi/irssi
- Si bien no entregué la tarea 2, siento que le puse demasiado empeño a esta tarea para salvar el ramo, profe confío en que lo hice bien :)


