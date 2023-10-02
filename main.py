from pynput import mouse, keyboard
import pyautogui as pg
import tkinter as tk
import customtkinter as ctk
import time

class App:

    def __init__(self) -> None:
        self.WIDTH = 900
        self.HEIGHT = 700
        self.master = ctk.CTk()
        self.master.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.master.title("Macro maker")
        self.master.resizable(False, False)

        self.master.mainloop()

if __name__ == "__main__":
    App()

