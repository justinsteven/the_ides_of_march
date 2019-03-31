FROM debian:stretch

COPY sleepy.sh /opt/sleepy.sh

RUN useradd -m -s /bin/bash attacker

RUN \
  apt-get update \
  && apt-get install -y \
    # For ncat
    nmap \
    # For SimpleHTTPServer
    python \
    --no-install-recommends \
  && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY gitpwn.git /www/totally_not_malicious.git
