import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog, Button, Text, Scrollbar, Frame, TOP, END, VERTICAL, Entry, Label


class Gui:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.root = tk.Tk()
        self.root.title("Online Store")
        self.root.attributes('-fullscreen', True)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.grid(row=0, column=0, sticky="nsew")
        self.tabs_list = []

        self.order_history_buttons = {}

    # method that adds a tab
    def add_tab(self, tab, text):
        self.tabs.add(tab, text=text)
        self.tabs_list.append(tab)

    #method that removes all the tabs
    def remove_tab(self, tab):
        if tab in self.tabs_list:
            self.tabs.forget(tab)
            self.tabs_list.remove(tab)

    def remove_tab_at_index(self, index):
        if 0 <= index < len(self.tabs_list):
            tab_to_remove = self.tabs_list[index]
            self.tabs.forget(tab_to_remove)
            self.tabs_list.pop(index)

    def clear_tabs(self):
        for tab in self.tabs_list:
            self.tabs.forget(tab)
        self.tabs_list.clear()

    #method that removes all tabs
    def remove_all_tabs(self):
        for tab in self.tabs_list[:]:
            self.tabs.forget(tab)
        self.tabs_list.clear()

    def run(self):
        self.root.mainloop()
