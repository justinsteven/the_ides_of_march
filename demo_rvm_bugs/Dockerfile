FROM debian:stretch

ARG victim_uid=31337
ARG victim_gid=31337

RUN \
  # Add a non-root user with your UID/GID for X access
  groupadd -g ${victim_gid} victim \
  && useradd -m -s /bin/bash -u ${victim_uid} -g ${victim_gid} victim

RUN \
  apt-get update \
  # Install
  && apt-get install -y --no-install-recommends \
    # for POC development:
    procps \
    psmisc \
    strace \
    vim-gtk \
    # pop calc
    x11-apps \
  && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
  # stop vim from capturing the mouse
  && sed -i 's/^"\s*\(let\s*g:skip_defaults_vim.*\)/\1/g' /etc/vim/vimrc

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

WORKDIR /home/victim/
