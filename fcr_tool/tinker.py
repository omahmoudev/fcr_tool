import builtins
import queue
import threading
import tkinter as tk
import tkinter.font as tkfont
from tkinter.scrolledtext import ScrolledText
import os
import sys
import main

# ---------------- PyInstaller-safe resource path ----------------
def resource_path(rel_path: str) -> str:
    """
    Works for:
      - running as .py in a folder (rel_path next to script)
      - PyInstaller --onefile (rel_path extracted into sys._MEIPASS temp dir)
    """
    base_path = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_path, rel_path)

# ---------------- Windows taskbar icon reliability ----------------
# Helps Windows show the right taskbar icon instead of the generic quill.
if sys.platform.startswith("win"):
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("fcrtool.app")
    except Exception:
        pass

# ---------------- Queues ----------------
in_q = queue.Queue()
out_q = queue.Queue()

_original_input = builtins.input
_original_print = builtins.print

def patched_input(prompt=""):
    out_q.put(str(prompt))
    return in_q.get()

def patched_print(*args, sep=" ", end="\n", **kwargs):
    out_q.put(sep.join(map(str, args)) + end)

# ---------------- Window ----------------
root = tk.Tk()
root.title("FCR Tool")
root.geometry("980x640")
root.minsize(860, 560)

# ---------------- Fonts ----------------
families = set(tkfont.families())
font_family = "Comic Sans MS" if "Comic Sans MS" in families else "TkDefaultFont"
base = tkfont.nametofont("TkDefaultFont").cget("size")
font_size = max(13, int(base * 1.4))
APP_FONT = (font_family, font_size)
root.option_add("*Font", APP_FONT)

# ---------------- Theme ----------------
SKY = "#7ec8ff"
GRASS = "#35b44a"
SUN = "#ffd25a"

PANEL_BG = "#f8fbff"
PANEL_BORDER = "#1f3d4a"
TEXT_BG = "#ffffff"
TEXT_FG = "#0f2a33"

BTN_BG = "#2a86a6"
BTN_BG_ACTIVE = "#226d86"

# ---------------- Icons (script + onefile EXE) ----------------
try:
    png_path = resource_path("icon.png")
    if os.path.exists(png_path):
        _icon = tk.PhotoImage(file=png_path)
        root.iconphoto(True, _icon)
        root._icon_ref = _icon
except Exception:
    pass

if sys.platform.startswith("win"):
    try:
        ico_path = resource_path("icon.ico")
        if os.path.exists(ico_path):
            root.iconbitmap(ico_path)
    except Exception:
        pass

# ---------------- Run main in thread ----------------
def run_main():
    builtins.input = patched_input
    builtins.print = patched_print
    try:
        main.main()
    finally:
        builtins.input = _original_input
        builtins.print = _original_print
        try:
            root.after(0, root.destroy)
        except Exception:
            pass

# ---------------- Canvas ----------------
canvas = tk.Canvas(root, highlightthickness=0, bd=0)
canvas.pack(fill="both", expand=True)

def draw_background():
    canvas.delete("bg")
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    if w <= 2 or h <= 2:
        return
    canvas.create_rectangle(0, 0, w, h, fill=SKY, outline="", tags="bg")
    grass_h = int(h * 0.25)
    canvas.create_rectangle(0, h - grass_h, w, h, fill=GRASS, outline="", tags="bg")
    r = int(min(w, h) * 0.08)
    canvas.create_oval(20, 20, 20 + 2 * r, 20 + 2 * r, fill=SUN, outline="", tags="bg")

# ---------------- Panel ----------------
panel = tk.Frame(
    canvas,
    bg=PANEL_BG,
    bd=2,
    relief="solid",
    highlightthickness=2,
    highlightbackground=PANEL_BORDER,
    highlightcolor=PANEL_BORDER,
)
panel_window = canvas.create_window(0, 0, window=panel, anchor="nw")

def place_panel():
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    if w <= 2 or h <= 2:
        return
    margin = max(18, int(min(w, h) * 0.03))
    canvas.coords(panel_window, margin, margin)
    canvas.itemconfig(panel_window, width=w - margin * 2, height=h - margin * 2)

def on_resize(event=None):
    draw_background()
    place_panel()

root.bind("<Configure>", on_resize)

# ---------------- Layout ----------------
panel.grid_rowconfigure(1, weight=1)
panel.grid_columnconfigure(0, weight=1)

title = tk.Label(panel, text="FCR Tool", bg=PANEL_BG, fg=PANEL_BORDER)
title.grid(row=0, column=0, sticky="w", padx=18, pady=(16, 6))

output = ScrolledText(
    panel,
    wrap="word",
    bg=TEXT_BG,
    fg=TEXT_FG,
    bd=2,
    relief="solid",
    padx=16,
    pady=14,
)
output.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
output.configure(state="disabled")

# ---------------- Input ----------------
input_row = tk.Frame(panel, bg=PANEL_BG)
input_row.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))
input_row.grid_columnconfigure(0, weight=1)

# Padded entry shell
entry_shell = tk.Frame(
    input_row,
    bg=TEXT_BG,
    bd=2,
    relief="solid",
    highlightthickness=2,
    highlightbackground=PANEL_BORDER,
    highlightcolor=BTN_BG,
)
entry_shell.grid(row=0, column=0, sticky="ew", padx=(0, 12))
entry_shell.grid_columnconfigure(0, weight=1)

entry = tk.Entry(
    entry_shell,
    bg=TEXT_BG,
    fg=TEXT_FG,
    insertbackground=TEXT_FG,
    bd=0,
    relief="flat",
)
entry.grid(row=0, column=0, sticky="ew", padx=14, pady=12)

def quit_now():
    try:
        in_q.put("q")
    except Exception:
        pass
    try:
        root.destroy()
    except Exception:
        pass

def send(event=None):
    text = entry.get().strip()
    entry.delete(0, "end")
    if text.lower() == "q":
        quit_now()
        return
    in_q.put(text)

btn = tk.Button(
    input_row,
    text="Send",
    command=send,
    bg=BTN_BG,
    fg="white",
    activebackground=BTN_BG_ACTIVE,
    activeforeground="white",
    bd=2,
    relief="solid",
    padx=18,
    pady=10,
)
btn.grid(row=0, column=1)

entry.bind("<Return>", send)
entry.focus_set()

# ---------------- Output pump ----------------
def pump():
    while True:
        try:
            msg = out_q.get_nowait()
        except queue.Empty:
            break
        output.configure(state="normal")
        output.insert("end", msg)
        output.see("end")
        output.configure(state="disabled")
    root.after(40, pump)

threading.Thread(target=run_main, daemon=True).start()
pump()
root.mainloop()
