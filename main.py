from pynput import mouse, keyboard
from threading import Thread
from tkinter.filedialog import asksaveasfilename, askopenfilename
import pyautogui as pg
import customtkinter as ctk
import tkinter as tk
import time as tm

class CTkListbox:
    """Listbox widget made with CTkScrollableFrame and CTkButton"""

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
        button.grid(row=len(self.cells)-1, column=0, padx=5, ipady=1)

    def __reset_by_index(self, index: int) -> None:
        for i in range(index, len(self.cells)):
            gridcell = self.surf.grid_slaves(i, 0)
            if len(gridcell)==0:
                self.__create_new(self.cells[i])
            else:
                gridcell[0].configure(text=self.cells[i])

    def select(self, index: int) -> None:
        """Select the option"""
        if index != self.selected_cell:
            self.surf.grid_slaves(index, 0)[0].configure(fg_color=self.DEFAULT_COLOR)
            if self.selected_cell != -1:
                self.surf.grid_slaves(self.selected_cell, 0)[0].configure(fg_color="transparent")
            self.selected_cell = index
    
    def swap(self, index1: int, index2: int) -> None:
        """Swap two options"""
        if self.selected_cell == index1:
            self.select(index2)
        elif self.selected_cell == index2:
            self.select(index1)
        self.cells[index1], self.cells[index2] = self.cells[index2], self.cells[index1]
        self.surf.grid_slaves(index1, 0)[0].configure(text=self.cells[index1])
        self.surf.grid_slaves(index2, 0)[0].configure(text=self.cells[index2])
        
    def delete(self, index: int) -> None:
        """Delete option"""
        if index != -1:
            self.cells.pop(index)
            self.__reset_by_index(index)
            self.surf.grid_slaves(len(self.cells), 0)[0].destroy()
            gridcell =  self.surf.grid_slaves(self.selected_cell, 0)
            if len(gridcell)>0:
                gridcell[0].configure(fg_color="transparent")
            self.selected_cell = -1

    def insert(self, index: int= -1, text: str = "") -> None:
        """Insert option at given index"""
        if index == -1:
            self.cells.append(text)
            self.__create_new(text)
        else:
            self.cells.insert(index, text)
            self.__reset_by_index(index)

    def clear(self) -> None:
        """Remove all options"""
        for i in reversed(range(len(self.cells))):
            print(i, self.cells)
            self.selected_cell = i
            self.delete(i)
        self.selected_cell = -1
    
    def return_contents(self) -> list[str]:
        """Return all options as list of strings"""
        return self.cells

    def return_selected(self) -> int:
        """Return currently selected option's index"""
        return self.selected_cell
    
    def return_size(self) -> int:
        """Returns number of options"""
        return len(self.cells)

    def place(self, **kwargs) -> None:
        """Place listbox"""
        self.surf.place(**kwargs)



class App:

    def __init__(self) -> None:
        self.DEFAULT_BTN_COLOR = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
        self.WIDTH = 900
        self.HEIGHT = 700
        self.master = ctk.CTk()
        self.master.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.master.title("Macro maker")
        self.master.resizable(False, False)
        self.master.bind("<Down>", lambda e: self.move_command(False))
        self.master.bind("<Up>", lambda e: self.move_command(True))
        self.text_value = tk.StringVar(self.master, "")
        self.flag_move = False
        self.flag_loop = False
        self.flag_mouse_input = False
        self.flag_keyboard = False
        self.flag_mouse = False
        self.flag_working = False
        self.init_menu()

        self.mouse_listener = mouse.Listener(on_click=self.mouse_input, daemon=True)
        self.mouse_listener.start()
        self.key_listener = keyboard.Listener(on_press=self.keyboard_input, daemon=True)
        self.key_listener.start()

        def close_app() -> None:
            self.flag_working = False
            self.mouse_listener.stop()
            self.key_listener.stop()
            self.master.quit()
        self.master.protocol("WM_DELETE_WINDOW", close_app)

        self.master.mainloop()

    def save_commands(self) -> None:
        path = asksaveasfilename(defaultextension=".txt", 
            filetypes=[("text file (.txt)", ".txt")], 
            title="Save commands")
        if path == "":
            return
        text = "\n".join(self.commands_tablist.return_contents())
        file = open(path, "w")
        file.write(text)
        file.close()

    def load_commands(self) -> None:
        path = askopenfilename(defaultextension=".txt", 
            filetypes=[("text file (.txt)", ".txt")], 
            title="Save commands")
        if path == "":
            return
        file = open(path, "r")
        contents = [x.rstrip() for x in file.readlines()]
        self.commands_tablist.clear()
        for i in contents:
            self.commands_tablist.insert(text=i)
        
    def time_waiter(self, time: int|float) -> None:
        for i in range(int(time)):
            if not self.flag_working: break
            tm.sleep(1)
        tm.sleep(time-int(time))

    def mouse_input(self, x: float, y: float, button: str, pressed: bool) -> None:
        if self.flag_mouse:
            if not self.flag_mouse_input:
                input_type = "click"
            elif pressed:
                input_type = "press"
            else:
                input_type = "release"
            if self.flag_mouse_input or pressed:
                self.commands_tablist.insert(text=f"{button} {x} {y} {input_type}")

    def keyboard_input(self, key) -> None:
        if key == keyboard.Key.f6 and not self.flag_working:
            self.flag_mouse = not self.flag_mouse
        elif key == keyboard.Key.f7:
            self.flag_working = not self.flag_working
            if self.flag_working:
                Thread(target=self.run_commands,
                          daemon=True).start()
        elif not self.flag_working and self.flag_keyboard:
            text = str(key).strip("'").removeprefix("Key.")
            self.commands_tablist.insert(text="".join([x for x in text
                                                       if x != "_" or len(text)==1]))

    def move_command(self, up_or_down: bool) -> None:
        selected = self.commands_tablist.return_selected()
        if (selected<self.commands_tablist.return_size()-1 and
            self.flag_move and not up_or_down and selected != -1):
            self.commands_tablist.swap(selected, selected+1)
        elif (selected>0 and self.flag_move and up_or_down and selected != -1):
            self.commands_tablist.swap(selected, selected-1)

    def push_time_command(self) -> None:
        try:
            time = float(self.text_value.get())
        except Exception:
            time = 1
        if time == int(time): time = int(time)
        index = self.commands_tablist.return_selected()
        if index==None: self.commands_tablist.insert(-1, f"Time {time}")
        else: self.commands_tablist.insert(index, f"Time {time}")
    
    def push_text_command(self) -> None:
        word = self.text_value.get()
        word = "Word "+word if len(word)>1 else word
        index = self.commands_tablist.return_selected()
        if index==None: self.commands_tablist.insert(-1, word)
        else: self.commands_tablist.insert(index, word)

    def run_commands(self) -> None:
        command_list = [x.split() for x in self.commands_tablist.return_contents()]
        while True:
            if not self.flag_working: break
            for i in command_list:
                if not self.flag_working: break
                if i[0]=="Word":
                    pg.typewrite(" ".join(i[1:]), interval=0.05)
                elif i[0]=="Time":
                    self.time_waiter(float(i[1]))
                elif "Button" in i[0]:
                    if i[3] == "click":
                        pg.click(button=i[0].split(".")[1], x=int(i[1]), y=int(i[2]))
                    if i[3] == "press":
                        pg.mouseDown(button=i[0].split(".")[1], x=int(i[1]), y=int(i[2]))
                    else:
                        pg.mouseUp(button=i[0].split(".")[1], x=int(i[1]), y=int(i[2]))
                else:
                    pg.press(i[0])
            if not self.flag_loop: break
        self.flag_working = False

    def init_menu(self) -> None:
        # command list frame
        self.commands_frame = ctk.CTkFrame(self.master, height=self.HEIGHT-80,
            width=self.WIDTH//2-80, corner_radius=10)
        self.commands_frame.place(relx=0.25, rely=0.5, anchor='center')
        self.commands_tablist = CTkListbox(self.commands_frame, 
            width=self.WIDTH//2-160, height=self.HEIGHT-160)
        self.commands_tablist.place(relx=0.5, rely=0.5, anchor='center')
        
        # options frame
        self.options_frame = ctk.CTkFrame(self.master, width=self.WIDTH//2-20,
            height=240, corner_radius=10)
        self.options_frame.place(relx=0.72, rely=0.23, anchor='center')

        def switch_loop_mode(n: int) -> None: 
            self.flag_loop = bool(int(n))
        def switch_keyboard_mode(n: int) -> None:
            self.flag_keyboard = bool(int(n))
        def switch_move_mode(n: int) -> None:
            self.flag_move = bool(int(n))
        def switch_mouse_input_mode(n: int) -> None:
            self.flag_mouse_input = bool(int(n))

        ctk.CTkLabel(self.options_frame, width=100, height=40,
                     font=("Roboto", 18), text="Switch keyboard listener").place(
                         relx=0.03, rely=0.13, anchor='w')
        slider0 = ctk.CTkSlider(self.options_frame, width=50, height=25, from_=0,
                      to=1, number_of_steps=1, command=switch_keyboard_mode)
        slider0.place(relx=0.9, rely=0.13, anchor='center')
        slider0.set(0)

        ctk.CTkLabel(self.options_frame, width=100, height=40,
                     font=("Roboto", 18), text="Switch moving commands").place(
                         relx=0.03, rely=0.33, anchor='w')
        slider1 = ctk.CTkSlider(self.options_frame, width=50, height=25, from_=0,
                      to=1, number_of_steps=1, command=switch_move_mode)
        slider1.place(relx=0.9, rely=0.33, anchor='center')
        slider1.set(0)
        
        ctk.CTkLabel(self.options_frame, width=100, height=40,
                     font=("Roboto", 18), text="Switch executing commands in loop").place(
                         relx=0.03, rely=0.53, anchor='w')
        slider2 = ctk.CTkSlider(self.options_frame, width=50, height=25, from_=0,
                      to=1, number_of_steps=1, command=switch_loop_mode)
        slider2.place(relx=0.9, rely=0.53, anchor='center')
        slider2.set(0)

        ctk.CTkLabel(self.options_frame, width=100, height=40,
                     font=("Roboto", 18), text="Mouse input type").place(
                         relx=0.5, rely=0.73, anchor='center')
        ctk.CTkLabel(self.options_frame, width=100, height=40,
                     font=("Roboto", 18), text="click").place(
                         relx=0.35, rely=0.88, anchor='center')
        ctk.CTkLabel(self.options_frame, width=100, height=40,
                     font=("Roboto", 18), text="press/release").place(
                         relx=0.75, rely=0.88, anchor='center')
        slider3 = ctk.CTkSlider(self.options_frame, width=50, height=25, from_=0,
                      to=1, number_of_steps=1, command=switch_mouse_input_mode)
        slider3.place(relx=0.5, rely=0.88, anchor='center')
        slider3.set(0)

        # actions frame
        self.actions_frame = ctk.CTkFrame(self.master, width=self.WIDTH//2-20,
            height=150, corner_radius=10)
        self.actions_frame.place(relx=0.72, rely=0.54, anchor='center')
        ctk.CTkEntry(self.actions_frame, width=300, height=30, 
                     textvariable=self.text_value, font=("Roboto", 18)).place(
                         relx=0.5, rely=0.2, anchor='center')
        ctk.CTkButton(self.actions_frame, width=180, height=30,
                      font=("Roboto", 18), text="Add time command",
                      command=self.push_time_command).place(
                         relx=0.27, rely=0.5, anchor='center') 
        ctk.CTkButton(self.actions_frame, width=180, height=30,
                      font=("Roboto", 18), text="Add word command",
                      command=self.push_text_command).place(
                         relx=0.73, rely=0.5, anchor='center') 
        ctk.CTkButton(self.actions_frame, width=180, height=30,
                      font=("Roboto", 18), text="Delete command",
                      command=lambda: self.commands_tablist.delete(
                          self.commands_tablist.return_selected())).place(
                         relx=0.27, rely=0.8, anchor='center') 
        
        # save frame
        self.save_frame = ctk.CTkFrame(self.master, width=self.WIDTH//2-20,
            height=80, corner_radius=10)
        self.save_frame.place(relx=0.72, rely=0.74, anchor='center')
        ctk.CTkButton(self.save_frame, width=180, height=30,
                      font=("Roboto", 18), text="Save commands",
                      command=self.save_commands).place(
                         relx=0.27, rely=0.5, anchor='center') 
        ctk.CTkButton(self.save_frame, width=180, height=30,
                      font=("Roboto", 18), text="Load commands",
                      command=self.load_commands).place(
                         relx=0.73, rely=0.5, anchor='center') 

        # notes frame
        self.notes_frame = ctk.CTkFrame(self.master, width=self.WIDTH//2-20,
            height=80, corner_radius=10)
        self.notes_frame.place(relx=0.72, rely=0.89, anchor='center')
        ctk.CTkLabel(self.notes_frame, width=self.WIDTH//2-100, height=60,
                     font=("Roboto", 16), text_color="#2583CD",
                     text="Press F6 to toggle mouse listener\nPress F7 to turn on/off macro",
                     justify='left', anchor='w').place(relx=0.05, rely=0.5, anchor='w')



if __name__ == "__main__":
    App()