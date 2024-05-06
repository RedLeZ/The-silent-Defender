import importlib
import os
import sys
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ReloadHandler(FileSystemEventHandler):
    def __init__(self, module):
        self.module = module

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print("Reloading module...")
            importlib.reload(self.module)


def main():
    import MainGame  # import your game module here

    handler = ReloadHandler(MainGame)
    observer = Observer()
    observer.schedule(handler, path=".", recursive=True)
    observer.start()

    try:
        MainGame.main()  # start your game here
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()
