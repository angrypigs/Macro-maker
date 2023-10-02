from pynput import mouse, keyboard
import pyautogui as pg
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
        # command list frame
        self.commands_frame = ctk.CTkFrame(self.master, height=self.HEIGHT-80,
            width=self.WIDTH//2-80, corner_radius=10)
        self.commands_frame.place(relx=0.25, rely=0.5, anchor='center')
        self.commands_tablist = CTkListbox(self.commands_frame, 
            width=self.WIDTH//2-160, height=self.HEIGHT-160)
        self.commands_tablist.place(relx=0.5, rely=0.5, anchor='center')
        # title frame
        self.title_frame = ctk.CTkFrame(self.master, width=self.WIDTH//2-80,
            height=80, corner_radius=10)
        self.title_frame.place(relx=0.75, rely=0.11, anchor='center')
        ctk.CTkLabel(self.title_frame, height=60, width=self.WIDTH//2-80,
                     font=("Roboto", 32), text="Macro maker"
                     ).place(relx=0.5, rely=0.5, anchor='center')
        # options frame
        self.options_frame = ctk.CTkFrame(self.master, width=self.WIDTH//2-80,
            height=160, corner_radius=10)
        self.options_frame.place(relx=0.75, rely=0.32, anchor='center')
        # time frame
        self.time_frame = ctk.CTkFrame(self.master, width=self.WIDTH//2-80,
            height=120, corner_radius=10)
        self.time_frame.place(relx=0.75, rely=0.56, anchor='center')
        # save frame
        self.save_frame = ctk.CTkFrame(self.master, width=self.WIDTH//2-80,
            height=80, corner_radius=10)
        self.save_frame.place(relx=0.75, rely=0.74, anchor='center')
        # notes frame
        self.notes_frame = ctk.CTkFrame(self.master, width=self.WIDTH//2-80,
            height=80, corner_radius=10)
        self.notes_frame.place(relx=0.75, rely=0.89, anchor='center')
        ctk.CTkLabel(self.notes_frame, width=self.WIDTH//2-100, height=60,
                     font=("Roboto", 16), text_color="#2583CD",
                     text="Press F6 to toggle keyboard/mouse listener\nPress F7 to turn on/off macro",
                     justify='left', anchor='w').place(relx=0.5, rely=0.5, anchor='center')



if __name__ == "__main__":
    App()