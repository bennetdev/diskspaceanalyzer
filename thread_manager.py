
class Ready:
    def __init__(self, directoryReader, view, thread):
        self.directoryReader = directoryReader
        self.view = view
        self.thread = thread
    def check_read_state(self):
        self.thread.join()
        self.view.show_dirs()
    def start_after_thread(self):
        self.thread.join()
        self.view.start()