#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from settings.config_default import BASE_DIR


class Watcher:
    DIRECTORY_TO_WATCH = join(BASE_DIR, 'books/JsonFrench')
    #  DIRECTORY_TO_WATCH = '/home/alassane/Code/JimBot/chatbotapp' + '/books'

    def __init__(self):
        self.observer = Observer() # Create Observer

    def run(self):
        event_handler = Handler() # todo on Event
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Salut Yattara ! Error watcher can't cannot observe.")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event :" + event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event :" + event.src_path)

        elif event.event_type == 'deleted':
            # Taken any action here when a file is deleted.
            print("Received deleted event :" + event.src_path)


if __name__ == '__main__':
    w = Watcher()
    w.run()
