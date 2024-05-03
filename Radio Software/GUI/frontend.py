import tkinter as tk
from tkinter import ttk
from tkinter import constants
from tkinter import messagebox
from PIL import Image, ImageTk

from engine_frame import engine_frame as ef
from primary_frame import primary_frame as pf
from secondary_frame import secondary_frame as sf
from misc_frame import misc_frame as mf

class frontend:
    width = 1600
    height = 900
    frame_width = 20

    is_logging = False

    def __init__(self):
        self.window = tk.Tk()

        self.window.title = "Cal Poly Baja SAE Live Data"
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.configure(bg="#DFEFFF")

        self.window.rowconfigure(0, weight=100)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=10)
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)
        self.window.columnconfigure(3, weight=1)

        style = ttk.Style(self.window)
        style.configure("frame.TFrame", background="white")
        style.configure("label.TLabel", background="white")
        style.configure("credits.TLabel", background="#DFEFFF")
        style.configure("image.TLabel", background="#DFEFFF")
        style.configure("button.TButton", background="white", font=('Helvetica', 24))

        engineFrame = ttk.Frame(self.window, style="frame.TFrame", padding=10, relief=constants.GROOVE)
        engineFrame.grid(row=0, column=0, sticky="N")
        self.engineFrameManager = ef(engineFrame, self.frame_width)

        primaryFrame = ttk.Frame(self.window, style="frame.TFrame", padding=10, relief=constants.GROOVE)
        primaryFrame.grid(row=0, column=1, sticky="N")
        self.primaryFrameManager = pf(primaryFrame, self.frame_width)

        secondaryFrame = ttk.Frame(self.window, style="frame.TFrame", padding=10, relief=constants.GROOVE)
        secondaryFrame.grid(row=0, column=2, sticky="N")
        self.secondaryFrameManager = sf(secondaryFrame, self.frame_width)

        miscFrame = ttk.Frame(self.window, style="frame.TFrame", padding=10, relief=constants.GROOVE)
        miscFrame.grid(row=0, column=3, sticky="N")
        self.miscFrameManager = mf(miscFrame, self.frame_width)

        self.log_toggle_button = ttk.Button(self.window, style="button.TButton", text="Start Logging", command=self.on_toggle_logging)
        self.log_toggle_button.grid(row=1, rowspan=2, column=1, columnspan=2)

        credits_label = ttk.Label(self.window, style="image.TLabel", text="Created by Lauren Jones and Rahul Goyal ;)", font=('Helvetica', 14))
        credits_label.grid(row=1, column=3)

        cpr_logo_image = ImageTk.PhotoImage(image=Image.open("./frontend/cpr_logo.png").resize((360,65)))
        cpr_logo_label = ttk.Label(self.window, style="image.TLabel", image=cpr_logo_image)
        cpr_logo_label.image = cpr_logo_image
        cpr_logo_label.grid(row=2, column=3)

    def error_callback(self, message):
        messagebox.showerror("Error!", message)

    def setup(self, request_callback, command_callback):
        self.request_callback = request_callback
        self.command_callback = command_callback

    def run(self):
        self.window.after(100, self.request_callback)
        self.window.mainloop()

    def update_data(self, data):
        self.response_callback(data)

    def response_callback(self, data):
        self.window.after(100, self.request_callback)

        self.engineFrameManager.update(data)
        self.primaryFrameManager.update(data)
        self.secondaryFrameManager.update(data)
        self.miscFrameManager.update(data)

    def on_toggle_logging(self):
        self.is_logging = not self.is_logging

        if self.is_logging:
            self.log_toggle_button["text"] = "Stop Logging"
        else:
            self.log_toggle_button["text"] = "Start Logging"

        self.command_callback(self.is_logging)
