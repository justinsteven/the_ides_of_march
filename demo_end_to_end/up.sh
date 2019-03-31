#!/bin/bash

cat <<"EOF"
WARNING

The victim container will have SYS_PTRACE capability. This might allow for
container escape.

The victim container will have access to your host's X socket. This allows for
container escape.

Malicious code running in this container might try to escape to your host.
EOF

read -p "Do you want to continue? [yN] " -r

if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
  exit 1
fi

my_dir=$(dirname "$(readlink -f "$0")")

cd "$my_dir"
sudo -g docker docker-compose rm -f
sudo -g docker victim_uid="$(id -u)" victim_gid="$(id -g)" docker-compose up --build
