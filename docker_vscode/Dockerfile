FROM debian

ARG my_uid=31337
ARG my_gid=31337
ARG my_username=justin

RUN \
  # Add a non-root user with your UID/GID for X access
  groupadd -g ${my_gid} ${my_username} \
  && useradd -m -s /bin/bash -u ${my_uid} -g ${my_gid} ${my_username}

RUN \
  apt-get update \
  && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    gnupg \
    # required by Microsoft's APT repo:
    apt-transport-https \
    # runtime requirements for code:
    libasound2 \
    libgconf-2-4 \
    libgtk2.0-0 \
    libxss1 \
    libxtst6 \
  && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN \
  curl -fsS https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | apt-key add - \
  && echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list \
  && apt-get update \
  && apt-get install -y --no-install-recommends \
    code \
  && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

USER ${my_username}

WORKDIR /home/${my_username}/
