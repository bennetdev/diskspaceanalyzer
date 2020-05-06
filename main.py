from directoryReader import DirectoryReader
import tkinter as tk
from gui import View

root = tk.Tk()
view = View(root, 800, 800)
root.mainloop()

directory_reader = DirectoryReader("C:\\")
directory_reader.read_dir()
level = 0
while True:
    directory_reader.ausgabe()
    next_index = int(input("Naechster Index"))
    if next_index == 1337:
        directory_reader.last_path(level)
        level -= 1
    else:
        directory_reader.next_path(level, next_index)
        directory_reader.read_dir()
        level += 1

