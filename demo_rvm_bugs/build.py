#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
import getpass

whoami = getpass.getuser()

# Dirty hack
if whoami == "justin":
  NS = "justinsteven"
else:
  NS = whoami

IMAGE = "rvm:1.28.0"

parser = argparse.ArgumentParser(
  description="build {0}/{1}".format(NS, IMAGE),
  epilog="@justinsteven"
)

parser.add_argument(
  "--clean",
  action="store_true",
  help="Build from scratch (Invalidate the cache)"
)

args = parser.parse_args()

print("[+] cd'ing in to build context")
os.chdir(os.path.dirname(os.path.realpath(__file__)))

run = [
    "sudo",
    "docker",
    "build",
    "--build-arg=victim_uid={}".format(os.getuid()),
    "--build-arg=victim_gid={}".format(os.getgid()),
    "--tag={}/{}".format(NS, IMAGE),
  ]

if args.clean:
  print("[+] building image {0}/{1} clean (invalidating cache)".format(NS, IMAGE))
  print("Are you sure? (Ctrl-C to abort)")
  input()
  run.append("--no-cache")
  run.append("--pull")
else:
  print("[+] building image {0}/{1}".format(NS, IMAGE))

run.append(".")

print("Doing: {}".format(run))

res = subprocess.call(run)

sys.exit(res)
