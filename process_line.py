
import subprocess

class ProcessLine:
  def __init__(self):
    self.process = None

  def terminate_process(self):
    p = self.process
    if p and p.poll() == None:
      p.terminate()
  
  def run_process(self, cmds):
    cwd = "."
    for cmd in cmds:
      args = cmd.split()
      if args[0] == "cd":
        cwd = args[1]
      else:
        self.process = subprocess.Popen(args, cwd=cwd)
        status_code = self.process.wait()
        if status_code != 0: break
