import os



class DirectoryReader():
    def __init__(self):
        self.path = "C:\\"
        self.sub_dirs = []
        self.sub_dirs_sizes = []
        self.sizes_percent = []
        self.dir_sizes = []
        self.level = -1

    def read_dir(self):
        sub_dirs = []
        sub_dirs_sizes = []
        for root, dirs, files in os.walk(self.path):
            if root != self.path:
                break
            for dir in dirs:
                sub_dir = os.path.join(root, dir)
                print("root: " + root, "dir: " + dir, sub_dir)
                sub_dirs.append(sub_dir)
                sub_dirs_sizes.append(self.get_dir_size(sub_dir))
        self.sub_dirs.append(sub_dirs)
        self.sub_dirs_sizes.append(sub_dirs_sizes)
        self.level += 1
        self.set_current_dir_size()
        self.set_sizes_percent()
        self.sort_dirs_by_size()

    def get_dir_size(self, path):
        folder_size = 0
        for root, dirs, files in os.walk(path):
            for file_name in files:
                file = os.path.join(root, file_name)
                if len(file) > 255:
                    file = "\\\\?\\" + file
                folder_size += os.path.getsize(file)
        folder_size /= (1024 * 1024)
        folder_size = round(folder_size, 2)
        return folder_size

    def change_dir(self, path):
        self.path = path

    def set_current_dir_size(self):
        size = 0
        for root, dirs, files in os.walk(self.path):
            if root != self.path:
                break
            for file_name in files:
                file = os.path.join(root, file_name)
                if len(file) > 255:
                    file = "\\\\?\\" + file
                size += os.path.getsize(file)
        size /= (1024 * 1024)
        size = round(size, 2)
        self.sub_dirs[self.level].append("Files")
        self.sub_dirs_sizes[self.level].append(size)

    def last_path(self):
        new_sub_dirs = []
        new_sub_dirs_sizes = []
        new_sizes_percent = []
        for index, dirs in enumerate(self.sub_dirs):
            if index == self.level:
                break
            new_sub_dirs.append(dirs)
            new_sub_dirs_sizes.append(self.sub_dirs_sizes[index])
            new_sizes_percent.append(self.sizes_percent[index])
        self.sub_dirs = new_sub_dirs
        self.sub_dirs_sizes = new_sub_dirs_sizes
        self.sizes_percent = new_sizes_percent
        self.level -= 1


    def next_path(self, index):
        self.change_dir(self.get_path_by_index(index))

    def get_path_by_index(self, index):
        return self.sub_dirs[self.level][index]

    def set_sizes_percent(self):
        for index, sizes in enumerate(self.sub_dirs_sizes):
            if index >= len(self.sizes_percent):
                sizes_sum = 0
                sizes_percent = []
                for size in sizes:
                    sizes_sum += size
                for size in sizes:
                    sizes_percent.append(round(size / sizes_sum, 4))
                self.sizes_percent.append(sizes_percent)

    def sort_dirs_by_size(self):
        dirs_sorted = []
        sizes_sorted = []
        for index, dir in enumerate(self.sub_dirs):
            size_sorted, dir_sorted = (list(t) for t in zip(*sorted(zip(self.sub_dirs_sizes[index], dir), reverse=True)))
            dirs_sorted.append(dir_sorted)
            sizes_sorted.append(size_sorted)
        self.sub_dirs = dirs_sorted
        self.sub_dirs_sizes = sizes_sorted
        self.sizes_percent = []
        self.set_sizes_percent()

