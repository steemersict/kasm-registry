#!/usr/bin/env bash
set -ex
# Start Ferdium en herstart hem als hij sluit (patroon van de officiële Kasm-images)
START_COMMAND="/opt/Ferdium/ferdium"
PGREP="ferdium"
export MAXIMIZE="true"
export MAXIMIZE_NAME="Ferdium"
MAXIMIZE_SCRIPT=$STARTUPDIR/maximize_window.sh
ARGS=${APP_ARGS:---no-sandbox}

if [ -z "$DISABLE_CUSTOM_STARTUP" ]; then
    set +x
    while true; do
        if ! pgrep -x $PGREP > /dev/null; then
            /usr/bin/filter_ready
            /usr/bin/desktop_ready
            set +e
            bash ${MAXIMIZE_SCRIPT} &
            $START_COMMAND $ARGS
            set -e
        fi
        sleep 1
    done
fi
