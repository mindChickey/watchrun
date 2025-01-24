#!/usr/bin/python3

import sys
from watchrun import watch_dir_cmds

if __name__ == "__main__":
  argv = ["./ppp.py", "./qqq.py"]
  cmds = [f"{sys.executable} {arg}" for arg in argv]
  watch_dir_cmds("./dir", 1, cmds)
