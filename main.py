from pynput import mouse, keyboard
import pyautogui as pg
import tkinter as tk
import customtkinter as ctk
from CTkListbox import *
import time

class App:

    def __init__(self) -> None:
        self.WIDTH = 900
        self.HEIGHT = 700
        self.master = ctk.CTk()
        self.master.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.master.title("Macro maker")
        self.master.resizable(False, False)
        self.init_menu()
        self.master.mainloop()

    def init_menu(self) -> None:
        self.commands_frame = ctk.CTkFrame(self.master, height=self.HEIGHT-100,
            width=300)
        self.commands_frame.place(relx=0.2, rely=0.5, anchor=tk.CENTER)
        self.commands_tablist = CTkListbox(self.commands_frame, width=240,
                                           height=self.HEIGHT-160)
        self.commands_tablist.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

if __name__ == "__main__":
    App()

