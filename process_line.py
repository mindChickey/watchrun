
import subprocess

class ProcessLine:
  def __init__(self):
    self.process = None

  def terminate_process(self):
    p = self.process
    if p and p.poll() == None:
      p.terminate()
  
  def run_process(self, cmds):
    for cmd in cmds:
      self.process = subprocess.Popen(cmd.split())
      status_code = self.process.wait()
      if status_code != 0: break
