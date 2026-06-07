# ==================================
# Smart File Insight Engine
# Author: RaziyehDaryaee
# Language: Python
# GUI: Tkinter
#
# Description:
# Organizes files into folders
# based on their extensions.
# ==================================

import tkinter as tk
from tkinter import filedialog
import os
import shutil

# ---------------- MAIN WINDOW ----------------
screen = tk.Tk()
screen.title("Smart File Insight Engine")
screen.geometry("750x550+200+50")
screen.config(bg="#f4f4f4")
screen.iconbitmap("pic/file_29390.ico")
screen.resizable(False, False)

# ---------------- FILE TYPES ----------------
file_types = {
    "Images": [".jpg", ".png", ".jpeg"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Excel": [".xlsx", ".xls"],
    "Videos": [".mp4", ".wmv", ".avi"],
    "Music": [".mp3", ".wav"],
    "Zip": [".zip", ".rar"]
}

selected_folder = ""
files = []
counts = {}

# ---------------- LOG ----------------
def log(message):
    log_box.insert(tk.END, message + "\n")
    log_box.see(tk.END)

def clear_log():
    log_box.delete("1.0", tk.END)

# ---------------- MOVE FILE ----------------
def move_file(file, folder, target):
    target_folder = os.path.join(folder, target)

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    shutil.move(
        os.path.join(folder, file),
        os.path.join(target_folder, file)
    )

# ---------------- SELECT FOLDER ----------------
def select_folder():

    global selected_folder, files, counts

    folder = filedialog.askdirectory()
    if not folder:
        log("No folder selected")
        return

    selected_folder = folder
    path_lbl.config(text=folder)

    files = os.listdir(folder)

    counts = {k: 0 for k in file_types}
    counts["Others"] = 0

    for file in files:
        ext = os.path.splitext(file)[1].lower()
        found = False

        for cat, exts in file_types.items():
            if ext in exts:
                counts[cat] += 1
                found = True
                break

        if not found:
            counts["Others"] += 1

    report_lbl.config(
        text=f"""
Analysis Report

Images: {counts['Images']}
Documents: {counts['Documents']}
Excel: {counts['Excel']}
Videos: {counts['Videos']}
Music: {counts['Music']}
Zip: {counts['Zip']}
Others: {counts['Others']}
"""
    )

    log("Folder analyzed successfully")

# ---------------- CONFIRM MOVE ----------------
def confirm_move():

    if not selected_folder:
        log("Please select a folder first")
        return

    moved = 0

    for file in files:
        ext = os.path.splitext(file)[1].lower()
        found = False

        for cat, exts in file_types.items():
            if ext in exts:
                move_file(file, selected_folder, cat)
                log(f"{file} --> {cat}")
                found = True
                moved += 1
                break

        if not found:
            move_file(file, selected_folder, "Others")
            log(f"{file} --> Others")
            moved += 1

    log(f"Done ({moved} files moved)")

def hover(widget, enter_color, leave_color):
    def on_enter(e):
        widget.config(bg=enter_color)

    def on_leave(e):
        widget.config(bg=leave_color)

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

# ================= UI LAYOUT =================

# LEFT PANEL
left_frame = tk.Frame(screen, bg="#f4f4f4")
left_frame.place(x=20, y=20, width=160, height=520)

# ⭐ TITLE (NEW)
left_title = tk.Label(
    left_frame,
    text="FILE\nORGANIZER",
    font=("Arial", 16, "bold"),
    fg="#1f3b5c",
    bg="#f4f4f4",
    justify="center"
)
left_title.place(x=20, y=10)

# BUTTONS (shifted پایین‌تر به خاطر تیتر)
btn_select = tk.Button(
    left_frame,
    text="Select Folder",
    width=15,
    bg="#1f3b5c",
    fg="white",
    command=select_folder,


)
btn_select.place(x=10, y=80)
hover(btn_select, "#2c5aa0", "#1f3b5c")

btn_move = tk.Button(
    left_frame,
    text="Confirm Move",
    width=15,
    bg="#1f6f3b",
    fg="white",
    command=confirm_move
)
btn_move.place(x=10, y=130)
hover(btn_move, "#2f8a4a", "#1f6f3b")


btn_clear = tk.Button(
    left_frame,
    text="Clear Log",
    width=15,
    bg="#8b1e1e",
    fg="white",
    command=clear_log
)
btn_clear.place(x=10, y=180)
hover(btn_clear, "#b52b2b", "#8b1e1e")

# PATH LABEL
path_lbl = tk.Label(
    left_frame,
    text="No folder selected",
    wraplength=140,
    bg="#f4f4f4",
    fg="#333"
)
path_lbl.place(x=10, y=240)

# ---------------- REPORT ----------------
report_frame = tk.Frame(screen, bg="white", relief="groove")
report_frame.place(x=200, y=20, width=530, height=200)

report_lbl = tk.Label(
    report_frame,
    text="Analysis Report",
    justify="left",
    bg="white",
    fg="#1f3b5c"
)
report_lbl.place(x=10, y=10)

# ---------------- LOG ----------------
log_frame = tk.Frame(screen, bg="white", relief="groove")
log_frame.place(x=200, y=240, width=530, height=300)

log_title = tk.Label(
    log_frame,
    text="Activity Log",
    font=("Arial", 12, "bold"),
    bg="white"
)
log_title.place(x=10, y=5)

scrollbar = tk.Scrollbar(log_frame)
scrollbar.place(x=500, y=40, height=230)

log_box = tk.Text(
    log_frame,
    yscrollcommand=scrollbar.set
)
log_box.place(x=10, y=40, width=480, height=230)

scrollbar.config(command=log_box.yview)

# ---------------- RUN ----------------
screen.mainloop()

