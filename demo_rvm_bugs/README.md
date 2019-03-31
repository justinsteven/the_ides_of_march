# Demo - RVM 1.28.0 vulnerabilities

Reference: <https://github.com/justinsteven/advisories/blob/master/2017_rvm_cd_command_execution.md>

This Docker image was developed and tested on a Debian Stretch host running
Docker-ce.

## Contents

* `Dockerfile` - specifies a simple Docker image containing RVM 1.28.0
* `build.py` - builds the above Dockerfile as an image
* `instantiate.py` - runs the built Docker image
* `rvm_1.28.0.tar.gz` - Vulnerable version of RVM to install within the Docker image

## Instructions

Review `build.py` and `instantiate.py`

Run `build.py`:

```
[justin@diablo ~/work/ides_of_march/demo_rvm_bugs]% ./build.py
[+] cd'ing in to build context
[+] building image justinsteven/rvm:1.28.0
Doing: ['sudo', 'docker', 'build', '--build-arg=victim_uid=31337', '--build-arg=victim_gid=31337', '--tag=justinsteven/rvm:1.28.0', '.']
Sending build context to Docker daemon  1.248MB
Step 1/9 : FROM debian:stretch
 ---> 2d337f242f07
Step 2/9 : ARG victim_uid=31337
 ---> Using cache
 ---> 598c9d20dce0
Step 3/9 : ARG victim_gid=31337
 ---> Using cache
 ---> 2aade3e9849c
Step 4/9 : RUN   groupadd -g ${victim_gid} victim   && useradd -m -s /bin/bash -u ${victim_uid} -g ${victim_gid} victim
 ---> Using cache
 ---> 997cba8f4c38
Step 5/9 : RUN   apt-get update   && apt-get install -y --no-install-recommends       x11-apps       procps       psmisc       strace       vim-gtk   && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*   && sed -i 's/^"\s*\(let\s*g:skip_defaults_vim.*\)/\1/g' /etc/vim/vimrc
 ---> Using cache
 ---> 077912d4dea7
Step 6/9 : COPY --chown=victim:victim rvm_1.28.0.tar.gz /home/victim/
 ---> Using cache
 ---> a0ea801cec9d
Step 7/9 : USER victim
 ---> Using cache
 ---> c49e4f16048b
Step 8/9 : RUN   cd $(mktemp -d)   && tar -xf /home/victim/rvm_1.28.0.tar.gz   && cd rvm-1.28.0   && ./install --auto-dotfiles   && grep 'Load RVM into a shell session' ~/.profile >> ~/.bashrc   && cd   && rm -f /home/victim/rvm_1.28.0.tar.gz   && rm -rf /tmp/* || true
 ---> Using cache
 ---> 32eade5a72ba
Step 9/9 : WORKDIR /home/victim/
 ---> Using cache
 ---> 32671f8942fb
Successfully built 32671f8942fb
Successfully tagged justinsteven/rvm:1.28.0
```

Run `instantiate.py`:

```
[justin@diablo ~/work/ides_of_march/demo_rvm_bugs]% ./instantiate.py
Doing: ['sudo', 'docker', 'run', '-ti', '--rm', '--volume=/etc/localtime:/etc/localtime:ro', '--cap-add=SYS_PTRACE', '--env=DISPLAY', '--volume=/tmp/.X11-unix:/tmp/.X11-unix:ro', 'justinsteven/rvm:1.28.0']
WARNING: This container has SYS_PTRACE capability. Might allow for container escape.
WARNING: This container has access to your hosts's X socket. This allows for container escape.
victim@7590a9417023:~$ 
```

## License

`rvm_1.28.0.tar.gz` is (c) 2009-2011 Wayne E. Seguin, 2011-2016 Michal Papis,
2016 Piotr Kuczynski. It is licensed under the Apache License, Version 2.0 and
was obtained from <https://github.com/rvm/rvm/tree/master>

All other code is (c) Justin Steven 2019 and is licensed under the Apache
License, Version 2.0. It is provided on an "as is" basis, without warranties or
conditions of any kind.
