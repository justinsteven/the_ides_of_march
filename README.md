# The IDEs of March

This is a collection of things related to my presentation "The IDEs of March",
presented at CrikeyCon and AusCERT in 2019.

# Abstract

Software is "eating the world", and in the era of DevOps, those who are cutting
the code often have privileged access to production systems and software
delivery pipelines. A developer's workstation is a fantastic place for an
adversary to "be" in 2019.

We're relentlessly and rightfully focused on secure design, code quality, and
killing bugs. Are we hearing the call to protect the people and systems
responsible for building and operating our squeaky clean code?

Through a in-depth breakdown of security bugs in client-side software
development tooling (which are used by developers and hackers alike) and some
crazy arm-waving and posturing about the CI/CD's and the Jenkinses, we'll
explore the insecurities of software development software. How might an
attacker gain control over a developer's workstation? What might they do once
they pop shell? And what can we possibly do to pursue business excellence
through end-to-end secure delivery of software?

# Contents:

* [`the_ides_of_march.pdf`](the_ides_of_march.pdf) - presentation slides
* [`demo_rvm_bugs`](demo_rvm_bugs/) - Docker image for RVM demo
* [`demo_vscode_workspace_git`](demo_vscode_workspace_git/) - Docker image for Visual Studio Code demo
* [`demo_end_to_end`](demo_end_to_end/) - Docker-compose setup for end-to-end demo
* [`docker_vscode`](docker_vscode/) - Docker image for the latest Visual Studio Code, some batteries included

# A warning regarding X and the `SYS_PTRACE` capability

The `instantiate.py` scripts included in this repository run Docker containers
with one or both of the following:

* The `SYS_PTRACE` capability to allow debugging and tracing of processes within the container
* Your X socket exposed to the contaner

The `SYS_PTRACE` capability *might* allow any malware within the Docker
container to unduly influence your host OS, or even to escape the container
entirely.

The X socket exposure *definitely* allows any malware within the Docker
container to unduly influence your host OS and to escape the container through
tricksy X gymnastics. See <https://youtu.be/o5cASgBEXWY?t=1011> for more on
this sorcery (hi metl)

The `demo_rvm_bugs` and `demo_vscode_workspace_git` Docker image specifications
do not contain malware, but they intentionally include old and vulnerable
software for demonstration purposes.

The `demo_end_to_end` Docker image specification contains exploits that
*should* not be dangerous - all of their activity should be confined to the
Docker-compose containers.

The `docker_vscode` contains no malware, nor any exploits, but you know. This
talk is all about vulnerabilities in software development software after all.
That said, the X socket exposure is almost certainly better than just running
VSCode directly on your host OS.

All code and all Docker image specifications are provided "as is" with no
warranties or guarantees.

# A note regarding SELinux and .Xauthority

These Docker images and the accompanying `instantiate.py` scripts were
developed and tested on a Debian Stretch host.

Some people have reported issues with the X exposure on other OS's such as
Fedora.

Some of these issues appear to relate to SELinux. See
<https://adam.younglogic.com/2017/01/gui-applications-container/> for potential
guidance on that front.

Some of these issues appear to relate to X requiring authentication via magic
cookies. See the following links for potential guidance on that front.

* <https://stackoverflow.com/a/51795708>; which references:
* <https://stackoverflow.com/a/25280523>

`docker_vscode/instantiate.py` has a `-x` or `--xauthority` flag that attempts
to implement the fix in the second link above. It may be of use if launching
`code` inside the container seems to do nothing.

It is not implemented for the demos. Doing so is an exercise left for the
reader :^)
