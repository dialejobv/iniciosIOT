# **NODEMCU V3-Instalando MicroPython-Uso en Thonny**
Nota: Thonny es un buen editor también para el manejo de los diferentes modelos de las esp8266, en este caso, se deben desarrollar diferentes pasos que se explicarán a continuación.

## Paso 1

El primer paso que se debe desarrollar es abrir la consola CMD (en el caso de windows), teniendo:

![image](https://github.com/user-attachments/assets/a95a39cf-596b-4b10-bf21-690ca7aabf20)


## Paso 2

Se debe escribir el siguiente comando: "pip install esptool", en dado caso que no sea reconocido python se debe revisar las variables de entorno del sistema y colocar la ruta del Path, para revisar en la consola CMD si está python, los estudiantes pueden escribir "python --version". Si al escribir pip aparece lo siguiente "pip no se reconoce como comando" es necesario que los estudiantes vuelvan a ingresar en las variables de entorno y revisen en el pc la dirección donde se ubica el pip, que generalmente está dentro de la carpeta de python. Se deja vídeo corto y sencillo donde se ecplica el proceso de reconocimiento de pip: [Detección de PIP](https://www.youtube.com/watch?v=XMvIAKcOJ_w). Luego de que sea detectado el pip si se debe proceder a escribir **pip install esptool**.

## Paso 3

Se debe ir a la página oficial de [micropython](https://micropython.org/), luego se deben dirigir a la zona de descargas y escoger la opción esp82266 y descargar la versión más actualizada, se deja el enlace para que los estudiantes se dirijan allá: [ESP8266](https://micropython.org/download/ESP8266_GENERIC/).

![image](https://github.com/user-attachments/assets/1b30ecff-f183-4015-9a0b-6fe2cfb1e52a)


## Paso 4

Luego de generar la descarga los estudiantes deben revisar en el **administrador de dispositivos** cuál es el puerto **com** donde fue detectado el sistema embebido y deben proceder a escribir el siguiente comando: **esptool --chip esp8266 -p comN erase_flash** donde en comN N es el número del puerto.

![image](https://github.com/user-attachments/assets/d29c82b6-5bac-4155-b3d1-84915f82d185)


## Paso 5

Luego de escribir ese comando, se deben dirigir a la zona de descargas donde se desarrolló las descarga del archivo de la página oficial de MicroPython y se debe escribir el siguiente comando: "esptool --chip esp8266 -p comN --baud 115200 write_flash --flash_size=detect -fm dio 0 ESP8266_GENERIC-20241129-v1.24.1.bin", se comparte pantallazo para que no existan dudas del proceso:

![image](https://github.com/user-attachments/assets/f1e4994b-2a73-4b43-8c68-db53204770a0)

## Paso 6

Posteriormente se abre thonny, se escoge la opción de ejecutar y se escoge **configurar intérprete** donde se selecciona lo siguiente:

![image](https://github.com/user-attachments/assets/a356deac-44e1-48b8-9aa4-770d9a2f203a)

Y luego se da ok y se puede empezar a trabajar con el sistema embebido y se puede probar diferentes códigos.
