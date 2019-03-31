# Visual Studio Code within Docker

This is a specification for a Visual Studio Code Docker image.

The included `instantiate.py` script runs the Docker image. It takes an
optional `-d` or `--directory` command-line flag to map one or more directories
from your host filesystem into the Docker container.

You may find this useful for running a nicely isolated and segmented instance
of Visual Studio Code. Barring a Docker escape vulnerability, or abuse of the
exposed X socket (see notice below), malware running within the container
*should* not be able to access files on your host (unless you explicitly map
them in).

This Docker image was developed and tested on a Debian Stretch host running
Docker-ce.

## Warranty

There are absolutely NO warranties or guarantees provided for this Dockerfile
or its supporting Python scripts. They are provided "as is".  It is your
responsibility to determine if they are fit for purpose, and if using them is
right for you.

## X attack surface

The included `instantiate.py` script runs the Docker image as a container, and
maps your host's X socket in to the container. This presents a security risk.
If the Docker container becomes compromised, then malware is able to spy on
your host's activity and can escape through various X gymnastics.

For an excellent demonstration of this attack surface, see
<https://youtu.be/o5cASgBEXWY?t=1011>

## Telemetry

Microsoft collects telemetry and crash reporting from Visual Studio Code by
default. See
<https://code.visualstudio.com/docs/supporting/FAQ#_how-to-disable-telemetry-reporting>
for more info.

You may wish to disable this. As of the time of writing this README, this can
be reportedly be done by setting the following keys to `false` in
`~/.config/Code/User/settings.json` of the Docker image during the build
process.

* `"telemetry.enableTelemetry"`
* `"telemetry.enableCrashReporter"`

This has NOT been done for you, and is left as an exercise for the user.

## Software

The following software is installed as specified by the Dockerfile:

* curl
* git
* Visual Studio Code

You may wish to add other software depending on your needs (e.g.  nodejs, php,
etc.)

## Contents of this directory

* `Dockerfile` - specifies a simple Docker image that will install the latest VSCode from Microsoft
* `build.py` - builds the above Dockerfile as an image
* `instantiate.py` - runs the built Docker image

## Instructions

Review `build.py` and `instantiate.py`

Run `build.py`:

```
[justin@diablo ~/work/ides_of_march/docker_vscode]% ./build.py
[+] cd'ing in to build context
[+] building image justinsteven/vscode:latest
Doing: ['sudo', 'docker', 'build', '--build-arg=my_uid=31337', '--build-arg=my_gid=31337', '--build-arg=my_username=justin', '--tag=justinsteven/vscode:latest', '.']
Sending build context to Docker daemon  35.33kB
Step 1/9 : FROM debian
 ---> d508d16c64cd
Step 2/9 : ARG my_uid=31337
 ---> Using cache
 ---> 67c17ad28bf6
Step 3/9 : ARG my_gid=31337
 ---> Using cache
 ---> f6bc11355f92
Step 4/9 : ARG my_username=justin
 ---> Using cache
 ---> ca01100d2e89
Step 5/9 : RUN   groupadd -g ${my_gid} ${my_username}   && useradd -m -s /bin/bash -u ${my_uid} -g ${my_gid} ${my_username}
 ---> Using cache
 ---> 76bc6ba0ffbc
Step 6/9 : RUN   apt-get update   && apt-get install -y --no-install-recommends     ca-certificates     curl     git     gnupg     apt-transport-https     libasound2     libgconf-2-4     libgtk2.0-0     libxss1     libxtst6   && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
 ---> Using cache
 ---> 3475d3ea27c3
Step 7/9 : RUN   curl -fsS https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | apt-key add -   && echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list   && apt-get update   && apt-get install -y --no-install-recommends     code   && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
 ---> Using cache
 ---> 3ae991fc787d
Step 8/9 : USER ${my_username}
 ---> Using cache
 ---> 3beb426a4c10
Step 9/9 : WORKDIR /home/${my_username}/
 ---> Using cache
 ---> e2a270714067
Successfully built e2a270714067
Successfully tagged justinsteven/vscode:latest
```

Run `instantiate.py`:

```
[justin@diablo ~/work/ides_of_march/docker_vscode]% ./instantiate.py
Doing: ['sudo', 'docker', 'run', '-ti', '--rm', '--volume=/etc/localtime:/etc/localtime:ro', '--env=DISPLAY', '--volume=/tmp/.X11-unix:/tmp/.X11-unix:ro', 'justinsteven/vscode:latest']
WARNING: This container has access to your hosts's X socket. This allows forcontainer escape.
justin@37a8c677d599:~$ 
```

## Mapping directories

You can use the optional `-d` or `--directories` command-line flag to map one
or more directories from your host's filesystem into the Docker container.

If you map only one directory, it will be made available at `~/project/` within
the container:

```
[justin@diablo ~/work/ides_of_march/docker_vscode]% ./instantiate.py --directory /etc/cron.weekly
Doing: ['sudo', 'docker', 'run', '-ti', '--rm', '--volume=/etc/localtime:/etc/localtime:ro', '--env=DISPLAY', '--volume=/tmp/.X11-unix:/tmp/.X11-unix:ro', '--volume=/etc/cron.weekly:/home/justin/project', 'justinsteven/vscode:latest']
WARNING: This container has access to your hosts's X socket. This allows for container escape.
justin@2b3b10b701eb:~$ ls ~/project
0anacron  man-db
```

If you map more than one directory, they will be made available at individual
`~/project_<something>/` directories within the container:

```
1:59:47[justin@diablo ~/work/ides_of_march/docker_vscode](master/!2?9)% ./instantiate.py --directory /etc/cron.weekly /etc/cron.monthly
Doing: ['sudo', 'docker', 'run', '-ti', '--rm', '--volume=/etc/localtime:/etc/localtime:ro', '--env=DISPLAY', '--volume=/tmp/.X11-unix:/tmp/.X11-unix:ro', '--volume=/etc/cron.weekly:/home/justin/project_cron.weekly', '--volume=/etc/cron.monthly:/home/justin/project_cron.monthly', 'justinsteven/vscode:latest']
WARNING: This container has access to your hosts's X socket. This allows for container escape.
justin@78f9bda022cd:~$ ls ~/project_*
/home/justin/project_cron.monthly:
0anacron

/home/justin/project_cron.weekly:
0anacron  man-db
```

## A note regarding SELinux and `.Xauthority`

Some people have reported issues with the X exposure on other OS's such as
Fedora.

Some of these issues appear to relate to SELinux. See
<https://adam.younglogic.com/2017/01/gui-applications-container/> for potential
guidance on that front.

Some of these issues appear to relate to X requiring authentication via magic
cookies. See the following links for potential guidance on that front.

* <https://stackoverflow.com/a/51795708>; which references:
* <https://stackoverflow.com/a/25280523>

`instantiate.py` has a `-x` or `--xauthority` flag that attempts to implement
the fix in the second link above. It may be of use if launching `code` inside
the container seems to do nothing.

```
[justin@diablo ~/work/ides_of_march/docker_vscode]% ./instantiate.py -x
Doing: ['sudo', 'docker', 'run', '-ti', '--rm', '--volume=/etc/localtime:/etc/localtime:ro', '--env=DISPLAY', '--volume=/tmp/.X11-unix:/tmp/.X11-unix:ro', '--volume=/tmp/.Xauthority_yhixgcbg:/home/justin/.Xauthority', 'justinsteven/vscode:latest']
WARNING: This container has access to your hosts's X socket. This allows for container escape.
justin@fe6281358e0b:~$ ls -la ~/.Xauthority
-rw------- 1 justin justin 51 Apr  1 18:33 /home/justin/.Xauthority
```

## License

The included Dockerfile automatically installs Visual Studio Code into the
resulting Docker image. Visual Studio Code is (c) Microsoft Corporation and is
licensed under the MIT License.

`build.py`, `instantiate.py` and the Dockerfile itself are (c) Justin Steven
2019 and are licensed under the Apache License, Version 2.0. They are provided
on an "as is" basis, without warranties or conditions of any kind.
