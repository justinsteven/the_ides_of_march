FROM debian:stretch

COPY sleepy.sh /opt/sleepy.sh

ARG victim_uid=31337
ARG victim_gid=31337

RUN \
  # Add a non-root user with your UID/GID for X access
  groupadd -g ${victim_gid} victim \
  && useradd -m -s /bin/bash -u ${victim_uid} -g ${victim_gid} victim

COPY --chown=victim:victim email.txt /home/victim/

# Install vulnerable git, plus netcat and other useful tools

COPY git_2.11.0-3+deb9u3_amd64.deb /tmp/
COPY git-man_2.11.0-3+deb9u3_all.deb /tmp/

RUN \
  apt-get update \
  && dpkg -i /tmp/git_2.11.0-3+deb9u3_amd64.deb /tmp/git-man_2.11.0-3+deb9u3_all.deb \
  # Resolve git's dependencies using -f
  ; apt-get install -f -y \
  && apt-get install -y \
    netcat-traditional \
    # for POC development:
    procps \
    psmisc \
    strace \
    vim-gtk \
    # pop calc
    x11-apps \
    --no-install-recommends \
  && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
  # stop vim from capturing the mouse
  && sed -i 's/^"\s*\(let\s*g:skip_defaults_vim.*\)/\1/g' /etc/vim/vimrc

# Install vulnerable vscode

COPY code_1.7.2-1479766213_amd64.deb /tmp/

RUN \
  apt-get update \
  && dpkg -i /tmp/code_1.7.2-1479766213_amd64.deb \
  # Resolve vscode's dependencies using -f
  ; apt-get install -f -y \
  && apt-get install -y --no-install-recommends \
    # runtime requirements for code:
    libgtk2.0-0 libxss1 libgconf-2-4 libasound2 \
  && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install vulnerable RVM

COPY --chown=victim:victim rvm_1.28.0.tar.gz /home/victim/

USER victim

RUN \
  cd $(mktemp -d) \
  && tar -xf /home/victim/rvm_1.28.0.tar.gz \
  && cd rvm-1.28.0 \
  && ./install --auto-dotfiles \
  # docker-run doesn't seem to source ~/.profile
  # we need to copy the RVM magic into .bashrc
  && grep 'Load RVM into a shell session' ~/.profile >> ~/.bashrc \
  && cd \
  && rm -f /home/victim/rvm_1.28.0.tar.gz \
  && rm -rf /tmp/* || true

USER root
WORKDIR /home/victim/
