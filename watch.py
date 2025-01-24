#!/usr/bin/python3

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from debounce import DebounceThread
from process_line import ProcessLine

class MyEventHandler(FileSystemEventHandler):
  def __init__(self, delay, immediate_callback, debounce_callback):
    self.debounce = DebounceThread(delay)
    self.immediate_callback = immediate_callback
    self.debounce_callback = debounce_callback

  def on_any_event(self, event: FileSystemEvent) -> None:
    self.immediate_callback()
    self.debounce.dispose(self.debounce_callback)

def watch_dir(path, delay, immediate_callback, debounce_callback):
  event_handler = MyEventHandler(delay, immediate_callback, debounce_callback)
  observer = Observer()
  observer.schedule(event_handler, path, recursive=True)
  observer.start()
  try:
    observer.join()
  except KeyboardInterrupt:
    observer.stop()

def watch_dir_cmds(path, delay, cmds):
  process_line = ProcessLine()
  immediate_callback = lambda: process_line.terminate_process()
  debounce_callback = lambda: process_line.run_process(cmds)
  watch_dir(path, delay, immediate_callback, debounce_callback)
