import tkinter as tk
from tkinter import *
from directoryReader import DirectoryReader
from tkinter import filedialog
import sys
import threading
from ready import Ready

class View:
    def __init__(self, master, width, height):
        self.width = width
        self.height = height
        self.master = master
        self.bar_height = 100



        master.title("MemoryAnalyzer")
        self.frame = tk.Frame(self.master, width=width, height=height)
        self.frame.pack(expand=True)
        self.colors = ["red", "green", "blue", "yellow", "black", "orange"]
        self.canvas = tk.Canvas(self.frame, width=800, height=500, scrollregion=(0, 0, 0, 500), bg="#1f4068")
        self.canvas.bind("<Button 1>", self.click_canvas)
        self.canvas.pack()
        self.master.bind_all("<MouseWheel>", self._on_mousewheel)
        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        self.scrollbar.pack(side=BOTTOM, fill=Y, expand=True)
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=LEFT, expand=True, fill=BOTH)
        self.rectangles = []
        self.labels = []
        self.menu = tk.Menu(self.master)
        self.menu.add_command(label="Pick Folder", command=self.pickFile)
        self.menu.add_command(label="Update", command=self.update_dirs)
        self.master.config(menu=self.menu)

    def pickFile(self):
        f = filedialog.askdirectory()
        if f == "":
            sys.exit(0)
        self.directory_reader = DirectoryReader()
        self.directory_reader.path = f.replace("/", "\\")
        self.start()

    def create_percent_bars(self, percents):
        self.canvas.delete("all")
        self.canvas.create_text(15, 10, text="Back", tag="back", fill="#dddddd")
        for index, per in enumerate(percents[self.directory_reader.level]):
            x1, y1, x2, y2 = self.get_percent_bar_cords(per, index)
            dir_path = self.directory_reader.sub_dirs[self.directory_reader.level][index]
            dir_name = dir_path.split("\\")[-1]
            if len(dir_name) > 12:
                while len(dir_name) > 12:
                    dir_name = dir_name[:-1]
                dir_name += "..."
            label = self.canvas.create_text(((x1 + x2) / 2, y2+10), text=dir_name, tag=index, fill="#dddddd")
            self.rectangles.append(self.canvas.create_rectangle(x1, y1, x2, y2, fill="#e43f5a", tag=index))

    def get_percent_bar_cords(self, percent, index):

        indices_in_row = 7.01
        index += 1
        percent = 1 - percent
        offset_y = int(index / indices_in_row)
        x1, y1, x2, y2 = 35, 50, 100, 200
        return x1 + (x2 * index) - (x2 * (indices_in_row) * offset_y), y1 + ((y2 - y1) * percent) + (y2 * offset_y), x2 * index - (x2 * (indices_in_row) * offset_y), y2 + (y2 * offset_y)

    def show_dirs(self):
        self.create_percent_bars(self.directory_reader.sizes_percent)
        rest_elements = len(self.rectangles) % 14
        scroll_size_y = int((len(self.rectangles) / 14)) * 400
        if rest_elements > 0 and rest_elements < 8:
            scroll_size_y += 250
        elif rest_elements > 0:
            scroll_size_y += 500
        print(scroll_size_y)

        self.canvas.config(scrollregion=(0, 0, 0, scroll_size_y))
    def start(self):
        thread = threading.Thread(name="thread1", target=self.directory_reader.read_dir)
        thread.start()
        ready = Ready(self.directory_reader, self, thread)
        thread_ready = threading.Thread(target=ready.check_read_state)
        thread_ready.start()


    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def update_dirs(self):
        path = self.directory_reader.path
        self.directory_reader = DirectoryReader()
        self.directory_reader.path = path
        self.start()

    def click_canvas(self, event):
        if self.canvas.find_withtag(CURRENT):
            tags = self.canvas.gettags(CURRENT)
            if tags[0] == "back":
                if self.directory_reader.level != 0:
                    thread_next = threading.Thread(name="thread_next", target=lambda: self.directory_reader.last_path())
                    ready = Ready(self.directory_reader, self, thread_next)
                    thread_ready = threading.Thread(target=ready.check_read_state)
                    thread_next.start()
                    thread_ready.start()
            else:
                index = int(tags[0])
                if self.directory_reader.sub_dirs[self.directory_reader.level][index] != "Files":
                    thread_next = threading.Thread(name="thread_next", target=lambda: self.directory_reader.next_path(index))
                    ready = Ready(self.directory_reader, self, thread_next)
                    thread_ready = threading.Thread(target=ready.start_after_thread)
                    thread_next.start()
                    thread_ready.start()

