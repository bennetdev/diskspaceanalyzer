import tkinter as tk
from tkinter import *
from directoryReader import DirectoryReader
from directoryReader import DirectoryReader
from tkinter import filedialog
from tkinter import ttk
import sys
import threading
from ready import Ready
import math

class View:
    def __init__(self, master, width, height):
        self.width = width
        self.height = height
        self.master = master
        self.bar_height = 100

        self.directory_reader = DirectoryReader()

        master.title("MemoryAnalyzer")
        self.frame = tk.Frame(self.master, width=width, height=height)
        self.frame.pack(expand=True)
        self.label = tk.Label(self.frame, text="Starte den Prozess um eine")
        self.label.pack(side=LEFT)
        self.colors = ["red", "green", "blue", "yellow", "black", "orange"]
        self.button = tk.Button(self.frame, text="Test", command=self.pickFile)
        self.button.pack(side=LEFT)
        self.canvas = tk.Canvas(self.frame, width=800, height=500, scrollregion=(0, 0, 0, 500), bg="grey")
        self.canvas.pack()
        self.master.bind_all("<MouseWheel>", self._on_mousewheel)
        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        self.scrollbar.pack(side=BOTTOM, fill=Y, expand=True)
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=LEFT, expand=True, fill=BOTH)
        self.rectangles = []
        self.labels = []

        # Draw some lines on it
        #self.canvas.create_line(0, 50, 800, 50)

        # Draw a rectangle bar 1
        #self.canvas.create_rectangle(35, 50, 100, 200, fill="red")

        # Draw a rectangle bar 2
        #canvas.create_rectangle(135, 125, 200, 200, fill="orange")

        # Draw a rectangle bar 3
        #canvas.create_rectangle(235, 50, 300, 200, fill="blue")

    def pickFile(self):
        f = filedialog.askdirectory()
        if f == "":
            sys.exit(0)

        self.directory_reader.path = f.replace("/", "\\")
        self.start()

    def create_percent_bars(self, percents):
        for index, per in enumerate(percents[self.directory_reader.level]):
            x1, y1, x2, y2 = self.get_percent_bar_cords(per, index)
            dir_path = self.directory_reader.sub_dirs[self.directory_reader.level][index]
            dir_name = dir_path.split("\\")[-1]
            if len(dir_name) > 12:
                while len(dir_name) > 12:
                    dir_name = dir_name[:-1]
                dir_name += "..."

            print(x1, x2, y1, y2, per)
            #print(per, self.colors[index], height)
            self.rectangles.append(self.canvas.create_rectangle(x1, y1, x2, y2, fill="red"))
            self.labels.append(self.canvas.create_text(((x1 + x2) / 2, y2+10), text=dir_name))
        #self.canvas.create_rectangle(135, 250, 100, 400, fill="green")

    def get_percent_bar_cords(self, percent, index):
        indices_in_row = 7.01
        index += 1
        percent = 1 - percent
        offset_y = int(index / indices_in_row)
        print(index / indices_in_row, offset_y)
        x1, y1, x2, y2 = 35, 50, 100, 200
        return x1 + (x2 * index) - (x2 * (indices_in_row) * offset_y), y1 + ((y2 - y1) * percent) + (y2 * offset_y), x2 * index - (x2 * (indices_in_row) * offset_y), y2 + (y2 * offset_y)

    def show_dirs(self):
        print(self.directory_reader.sizes_percent)
        self.create_percent_bars(self.directory_reader.sizes_percent)
        scroll_size_y = (((len(self.rectangles) - (len(self.rectangles) % 7)) / 7) + (len(self.rectangles) % 7)) * 500
        self.canvas.config(scrollregion=(0, 0, 0, scroll_size_y))
    def start(self):
        print("start")
        thread = threading.Thread(name="thread1", target=self.directory_reader.read_dir)
        thread.start()
        ready = Ready(self.directory_reader, self, thread)
        thread_ready = threading.Thread(target=ready.check_read_state)
        thread_ready.start()
        print(thread.is_alive())

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

root = tk.Tk()
view = View(root, 800, 800)
root.mainloop()