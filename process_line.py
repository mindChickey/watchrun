
import subprocess
import multiprocessing
from os import path

class ProcessLine:
  def __init__(self):
    self.process = None

  def terminate_process(self):
    p = self.process
    if p and p.poll() == None:
      p.terminate()
  
  def run_process(self, cmds):
    cwd = path.curdir
    for cmd in cmds:
      if isinstance(cmd, str):
        args = cmd.split()
        if args[0] == "cd":
          cwd = path.join(cmd, args[1])
        else:
          self.process = subprocess.Popen(args, cwd=cwd)
          status_code = self.process.wait()
          if status_code != 0: break

      elif callable(cmd):
        p = multiprocessing.Process(target=cmd)
        self.process = p
        p.start()
        p.join()
        if p.exitcode == 0:
          continue
        else:
          break
      
      else:
        raise "cmd type error"
