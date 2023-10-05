from pynput import mouse, keyboard
import pyautogui as pg
import customtkinter as ctk
import tkinter as tk
import time as tm

class CTkListbox:

    def __init__(self, master, width: int, height: int) -> None:
        self.surf = ctk.CTkScrollableFrame(master, width=width, height=height)
        self.DEFAULT_COLOR = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
        self.H = height
        self.W = width
        self.cells = []
        self.selected_cell = -1
    
    def __create_new(self, text: str) -> None:
        index = len(self.cells)-1
        button = ctk.CTkButton(self.surf, width=self.W-20, height=30, text=text,
                               command=lambda: self.select(index), 
                               fg_color="transparent", anchor="w", font=("Roboto", 16))
        button.grid(row=len(self.cells)-1, column=0, padx=5, pady=2)

    def __reset_by_index(self, index: int) -> None:
        for i in range(index, len(self.cells)):
            gridcell = self.surf.grid_slaves(i, 0)
            if len(gridcell)==0:
                self.__create_new(self.cells[i])
            else:
                gridcell[0].configure(text=self.cells[i])

    def select(self, index: int) -> None:
        if index != self.selected_cell:
            self.surf.grid_slaves(index, 0)[0].configure(fg_color=self.DEFAULT_COLOR)
            if self.selected_cell != -1:
                self.surf.grid_slaves(self.selected_cell, 0)[0].configure(fg_color="transparent")
            self.selected_cell = index

    def delete(self, index: int) -> None:
        self.cells.pop(index)
        self.__reset_by_index(index)
        self.surf.destroy(self.surf.grid_slaves(len(self.cells), 0)[0])

    def insert(self, index: int= -1, text: str = "") -> None:
        if index == -1:
            self.cells.append(text)
            self.__create_new(text)
        else:
            self.cells.insert(index, text)
            self.__reset_by_index(index)
    
    def return_contents(self) -> list:
        return self.cells

    def return_selected(self) -> int:
        return self.selected_cell

    def place(self, **kwargs) -> None:
        self.surf.place(**kwargs)

    

class App:

    def __init__(self) -> None:
        self.WIDTH = 900
        self.HEIGHT = 700
        self.master = ctk.CTk()
        self.master.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.master.title("Macro maker")
        self.master.resizable(False, False)
        self.time_value = tk.StringVar(self.master, "")
        self.commands_list = []
        self.init_menu()
        self.master.mainloop()

    def push_time_command(self) -> None:
        try:
            time = float(self.time_value.get())
        except Exception:
            time = 1
        if time == int(time): time = int(time)
        index = self.commands_tablist.return_selected()
        if index==None:
            self.commands_list.append(f"time {time}")
            self.commands_tablist.insert(-1, f"Time ({time})")
        else:
            self.commands_list.insert(index, f"time {time}")
            self.commands_tablist.insert(index, f"Time ({time})")

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
        ctk.CTkEntry(self.time_frame, width=180, height=30, 
                     textvariable=self.time_value, font=("Roboto", 18)).place(
                         relx=0.5, rely=0.3, anchor=tk.CENTER)
        ctk.CTkButton(self.time_frame, width=180, height=30,
                      font=("Roboto", 18), text="Add time command",
                      command=self.push_time_command).place(
                         relx=0.5, rely=0.7, anchor='center') 

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