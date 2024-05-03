import tkinter as tk
from tkinter import ttk

from data_frame import data_frame
from DataModel.eCVTData import eCVTData

class misc_frame:
    def __init__(self, frame, frame_width):
        data_names = [
            "Time",
            "-Brake Pressures",
            "Front Brake Pressure",
            "Rear Brake Pressure",
            "-Temperatures",
            "Primary Sheave Temp",
            "Primary Ambient Temp",
            "Primary Motor Temp",
            "Secondary Motor Temp",
            "-Vehicle",
            "eCVT Ratio",
            "Speed (mph)",
        ]

        self.frame = data_frame(frame, frame_width, data_names, "Miscellaneous")

    def update(self, ecvtData: eCVTData):
        self.frame.update("Time", f"{ecvtData.time // 60000000}m {ecvtData.time // 1000000 % 60}s")
        self.frame.update("Front Brake Pressure", ecvtData.fBrakePressure)
        self.frame.update("Rear Brake Pressure", ecvtData.rBrakePressure)
        self.frame.update("Primary Sheave Temp", ecvtData.pSheaveTemp)
        self.frame.update("Primary Ambient Temp", ecvtData.pAmbientTemp)
        self.frame.update("Primary Motor Temp", ecvtData.pMotorTemp)
        self.frame.update("Secondary Motor Temp", ecvtData.sMotorTemp)
        self.frame.update("eCVT Ratio", "∞" if (ecvtData.sSpeed == 0) else (ecvtData.pSpeed / ecvtData.sSpeed))
        self.frame.update("Speed (mph)", (ecvtData.sSpeed // 143))
