FROM debian:stretch

ARG victim_uid=31337
ARG victim_gid=31337

RUN \
  # Add a non-root user with your UID/GID for X access
  groupadd -g ${victim_gid} victim \
  && useradd -m -s /bin/bash -u ${victim_uid} -g ${victim_gid} victim

COPY code_1.7.2-1479766213_amd64.deb /tmp/

RUN \
  apt-get update \
  # Install old vscode
  && dpkg -i /tmp/code_1.7.2-1479766213_amd64.deb \
  # Resolve vscode's dependencies using -f
  ; apt-get install -f -y \
  # Install other packages
  && apt-get install -y --no-install-recommends \
    # for POC development:
    procps \
    psmisc \
    strace \
    vim-gtk \
    # pop calc
    x11-apps \
    # runtime requirements for code:
    libgtk2.0-0 libxss1 libgconf-2-4 libasound2 \
  && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
  # stop vim from capturing the mouse
  && sed -i 's/^"\s*\(let\s*g:skip_defaults_vim.*\)/\1/g' /etc/vim/vimrc

USER victim

WORKDIR /home/victim/
