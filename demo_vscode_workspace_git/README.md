# Demo - Visual Studio Code 1.7.2 vulnerabilities

Reference: <https://github.com/justinsteven/advisories/blob/master/2017_visual_studio_code_workspace_settings_code_execution.md>

This Docker image was developed and tested on a Debian Stretch host running
Docker-ce.

## Contents

* `Dockerfile` - specifies a simple Docker image containing VSCode 1.7.2
* `build.py` - builds the above Dockerfile as an image
* `instantiate.py` - runs the built Docker image
* `code_1.7.2-1479766213_amd64.deb` - Vulnerable version of VSCode to install within the Docker image

## Instructions

Review `build.py` and `instantiate.py`

Run `build.py`:

```
[justin@diablo ~/work/ides_of_march/demo_vscode_workspace_git]% ./build.py
[+] cd'ing in to build context
[+] building image justinsteven/vscode:1.7.2
Doing: ['sudo', 'docker', 'build', '--build-arg=victim_uid=31337', '--build-arg=victim_gid=31337', '--tag=justinsteven/vscode:1.7.2', '.']
Sending build context to Docker daemon  34.52MB
Step 1/8 : FROM debian:stretch
 ---> 2d337f242f07
Step 2/8 : ARG victim_uid=31337
 ---> Using cache
 ---> 7a49ae1fcca6
Step 3/8 : ARG victim_gid=31337
 ---> Using cache
 ---> bd7f437543bb
Step 4/8 : RUN   groupadd -g ${victim_gid} victim   && useradd -m -s /bin/bash -u ${victim_uid} -g ${victim_gid} victim
 ---> Using cache
 ---> c37e9c1899d3
Step 5/8 : COPY code_1.7.2-1479766213_amd64.deb /tmp/
 ---> Using cache
 ---> 8a3c2eaf74a7
Step 6/8 : RUN   apt-get update   && dpkg -i /tmp/code_1.7.2-1479766213_amd64.deb   ; apt-get install -f -y   && apt-get install -y --no-install-recommends       procps       psmisc       strace       vim-gtk       x11-apps       libgtk2.0-0 libxss1 libgconf-2-4 libasound2   && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*   && sed -i 's/^"\s*\(let\s*g:skip_defaults_vim.*\)/\1/g' /etc/vim/vimrc
 ---> Using cache
 ---> 300475b10dfb
Step 7/8 : USER victim
 ---> Using cache
 ---> 73944335a8d5
Step 8/8 : WORKDIR /home/victim/
 ---> Using cache
 ---> 24466a85d79f
Successfully built 24466a85d79f
Successfully tagged justinsteven/vscode:1.7.2
```

Run `instantiate.py`:

```
[justin@diablo ~/work/ides_of_march/demo_vscode_workspace_git]% ./instantiate.py
Doing: ['sudo', 'docker', 'run', '-ti', '--rm', '--volume=/etc/localtime:/etc/localtime:ro', '--cap-add=SYS_PTRACE', '--env=DISPLAY', '--volume=/tmp/.X11-unix:/tmp/.X11-unix:ro', 'justinsteven/vscode:1.7.2']
WARNING: This container has SYS_PTRACE capability. Might allow for container escape.
WARNING: This container has access to your hosts's X socket. This allows for container escape.
victim@b95aa6ba1d80:~$ 
```

## License

`code_1.7.2-1479766213_amd64.deb` is licensed, as follows, under the MIT
License.

```
MIT License

Copyright (c) 2015 - present Microsoft Corporation

All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

All other code is (c) Justin Steven 2019 and is licensed under the Apache
License, Version 2.0. It is provided on an "as is" basis, without warranties or
conditions of any kind.
