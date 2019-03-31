#!/usr/bin/env python3
import os
import sys
import subprocess
import getpass

whoami = getpass.getuser()

# Dirty hack
if whoami == "justin":
  NS = "justinsteven"
else:
  NS = whoami

IMAGE = "rvm:1.28.0"

run = [
    "sudo",
    "docker",
    "run",
    "-ti",
    "--rm",
    "--volume=/etc/localtime:/etc/localtime:ro",
    "--cap-add=SYS_PTRACE",
    "--env=DISPLAY",
    "--volume=/tmp/.X11-unix:/tmp/.X11-unix:ro",
    "{}/{}".format(NS, IMAGE)
  ]

print("Doing: {}".format(run))

if "--cap-add=SYS_PTRACE" in run:
  print("WARNING: This container has SYS_PTRACE capability. Might allow for container escape.")

if "--env=DISPLAY" in run:
  print("WARNING: This container has access to your hosts's X socket. This allows for container escape.")

res = subprocess.call(run)

sys.exit(res)
