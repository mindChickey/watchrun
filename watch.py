#!/usr/bin/python3

from os import path
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from .debounce import DebounceThread
from .process_line import ProcessLine

def inDirs(dirs, dir):
  d0 = path.abspath(dir)

  for d in dirs:
    if d == path.commonpath([d, d0]):
      return True
  return False

class MyEventHandler(FileSystemEventHandler):
  def __init__(self, delay, terminate_callback, start_callback, ignore_dirs=[]):
    self.debounce = DebounceThread(delay)
    self.terminate_callback = terminate_callback
    self.start_callback = start_callback
    self.ignore_dirs = [path.abspath(dir) for dir in ignore_dirs]

  def on_created(self, event: FileSystemEvent) -> None:
    if inDirs(self.ignore_dirs, event.src_path): return

    self.terminate_callback()
    self.debounce.dispose(self.start_callback)

  def on_deleted(self, event: FileSystemEvent) -> None:
    self.on_created(event)

  def on_modified(self, event: FileSystemEvent) -> None:
    self.on_created(event)

  def on_moved(self, event: FileSystemEvent) -> None:
    self.on_created(event)


def watch_dir(path, delay, terminate_callback, start_callback, ignore_dirs=[]):
  event_handler = MyEventHandler(delay, terminate_callback, start_callback, ignore_dirs)
  observer = Observer()
  observer.schedule(event_handler, path, recursive=True)
  observer.start()
  try:
    observer.join()
  except KeyboardInterrupt:
    observer.stop()

def watch_dir_cmds(path, delay, cmds, ignore_dirs=[]):
  process_line = ProcessLine()
  terminate_callback = lambda: process_line.terminate_process()
  start_callback = lambda: process_line.run_process(cmds)
  watch_dir(path, delay, terminate_callback, start_callback, ignore_dirs)
