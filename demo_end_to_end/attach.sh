#!/bin/bash

tmux_session=$(uuidgen)

tmux new-session -d -s "$tmux_session" sudo -g docker docker exec -ti -u victim:video --workdir=/home/victim/ demoendtoend_victim_1 bash

tmux split-window -t "${tmux_session}:1" sudo -g docker docker exec -ti demoendtoend_attacker_1 ncat -k -lvp 4444
tmux split-window -t "${tmux_session}:1" sudo -g docker docker exec -ti demoendtoend_attacker_1 ncat -k -lvp 4445
tmux split-window -t "${tmux_session}:1" sudo -g docker docker exec -ti demoendtoend_attacker_1 ncat -k -lvp 4446
tmux split-window -t "${tmux_session}:1" -h sudo -g docker docker exec -ti demoendtoend_attacker_1 sh -c 'cd /www && python -m SimpleHTTPServer 80'

tmux select-layout -t "${tmux_session}" main-vertical

tmux attach-session -t "$tmux_session"
