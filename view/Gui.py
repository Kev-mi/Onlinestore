import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog, Button, Text, Scrollbar, Frame, TOP, END, VERTICAL, Entry, Label


class Gui:
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor
        self.root = tk.Tk()
        self.root.title("Online Store")
        self.root.attributes('-fullscreen', True)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill=tk.BOTH, expand=True)
        self.tabs_list = []

    # method that adds a tab
    def add_tab(self, tab, text):
        self.tabs.add(tab, text=text)
        self.tabs_list.append(tab)

    #method that removes all the tabs
    def remove_tab(self, tab):
        if tab in self.tabs_list:
            self.tabs.forget(tab)
            self.tabs_list.remove(tab)

    #method that removes all tabs
    def remove_all_tabs(self):
        for tab in self.tabs_list[:]:
            self.tabs.forget(tab)
        self.tabs_list.clear()

    def run(self):
        self.root.mainloop()
