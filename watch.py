#!/usr/bin/python3

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from debounce import DebounceThread
from process_line import ProcessLine

class MyEventHandler(FileSystemEventHandler):
  def __init__(self, delay, terminate_callback, start_callback):
    self.debounce = DebounceThread(delay)
    self.terminate_callback = terminate_callback
    self.start_callback = start_callback

  def on_any_event(self, event: FileSystemEvent) -> None:
    self.terminate_callback()
    self.debounce.dispose(self.start_callback)

def watch_dir(path, delay, terminate_callback, start_callback):
  event_handler = MyEventHandler(delay, terminate_callback, start_callback)
  observer = Observer()
  observer.schedule(event_handler, path, recursive=True)
  observer.start()
  try:
    observer.join()
  except KeyboardInterrupt:
    observer.stop()

def watch_dir_cmds(path, delay, cmds):
  process_line = ProcessLine()
  terminate_callback = lambda: process_line.terminate_process()
  start_callback = lambda: process_line.run_process(cmds)
  watch_dir(path, delay, terminate_callback, start_callback)
