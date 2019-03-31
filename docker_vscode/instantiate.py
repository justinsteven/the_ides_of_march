#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess
import getpass
import tempfile
import atexit

whoami = getpass.getuser()

# Dirty hack
if whoami == "justin":
  NS = "justinsteven"
else:
  NS = whoami

IMAGE = "vscode:latest"

parser = argparse.ArgumentParser(
  description="run {0}/{1}".format(NS, IMAGE),
  epilog="@justinsteven"
)

parser.add_argument(
  "-d", "--directory",
  nargs="*",
  help="One or more directories to map into the container"
)

parser.add_argument(
  "-x", "--xauthority",
  action="store_true",
  help="Present ~/.Xauthority to the container (required for some host OS's)"
)

args = parser.parse_args()

directories = None

if args.directory:
  # Check each directory exists
  for d in args.directory:
    if not os.path.isdir(d):
      print("Directory {} does not exist".format(d))
      sys.exit(1)

  # Get absolute path of each directory
  directories = [os.path.abspath(x) for x in args.directory]

run = [
    "sudo",
    "docker",
    "run",
    "-ti",
    "--rm",
    "--volume=/etc/localtime:/etc/localtime:ro",
    "--env=DISPLAY",
    "--volume=/tmp/.X11-unix:/tmp/.X11-unix:ro",
  ]

if args.xauthority:
  # hat-tip to https://stackoverflow.com/a/51795708 and https://stackoverflow.com/a/25280523

  # Create a tempfile
  xauthority_fd, xauthority_filename = tempfile.mkstemp(prefix=".Xauthority_")

  # close() it
  os.close(xauthority_fd)

  # register it for deletion
  def delete_xauthority_file():
    os.remove(xauthority_filename)
  atexit.register(delete_xauthority_file)

  p1 = subprocess.Popen(["xauth", "nlist", os.getenv("DISPLAY")], stdout=subprocess.PIPE)
  p2 = subprocess.Popen(["sed", "s/^..../ffff/"], stdin=p1.stdout, stdout=subprocess.PIPE)
  p3 = subprocess.Popen(["xauth", "-f", xauthority_filename, "nmerge", "-"], stdin = p2.stdout)

  run.append("--volume={}:/home/{}/.Xauthority".format(xauthority_filename, whoami))


if directories:
  if len(directories) == 1:
    # Easy. Just map it to /home/$USERNAME/project
    run.append("--volume={}:/home/{}/project".format(
      directories[0],
      whoami
    ))
  else:
    """
      Tricky
      We'll map them to /home/$USERNAME/project_$BASENAME
      If we have colliding $BASENAME's we'll deconflict them
      Let's build a list of directory_mapping dicts
      These dicts will look like:
        {
          "directory": "$host_directory",
          "mapping": "project_${deconflicted_basename}"
        }
    """
    directory_mappings = []
    for directory in directories:
      directory_mapping = "project_{}".format(os.path.basename(directory))
      if any(filter(lambda x: x["mapping"] == directory_mapping, directory_mappings)):
        # We have a collsion
        # Deconflict it by appending _<n> and increment n until we no longer collide
        mapping_deconflictor = 1
        while any(filter(lambda x: x["mapping"] == "{}_{}".format(directory_mapping, mapping_deconflictor), directory_mappings)):
          mapping_deconflictor += 1
        directory_mappings.append({"directory": directory, "mapping": "{}_{}".format(directory_mapping, mapping_deconflictor)})
      else:
        directory_mappings.append({"directory": directory, "mapping": directory_mapping})
    for directory_mapping in directory_mappings:
      run.append("--volume={}:/home/{}/{}".format(
        directory_mapping["directory"],
        whoami,
        directory_mapping["mapping"]
      ))

run.append("{}/{}".format(NS, IMAGE))

print("Doing: {}".format(run))

if "--env=DISPLAY" in run:
  print("WARNING: This container has access to your hosts's X socket. This allows for container escape.")

res = subprocess.call(run)

sys.exit(res)
