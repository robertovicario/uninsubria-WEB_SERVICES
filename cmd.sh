#!/bin/bash

# Icons
ICON_START="▶"
ICON_STOP="■"
ICON_SETUP="◆"
ICON_RUN="●"
ICON_AUTH="◉"
ICON_DOWNLOAD="↓"
ICON_CLEAN="▽"
ICON_OK="✓"
ICON_ERR="✗"

# Colors
RED="\033[31m"
GREEN="\033[32m"
BLUE="\033[34m"
CYAN="\033[36m"
MAGENTA="\033[35m"
YELLOW="\033[33m"

# -------------------------

start() {
    printer -start "Starting the project..."

    # Docker
    docker compose start
    handler
}

stop() {
    printer -stop "Stopping the project..."

    # Docker
    docker compose stop
    handler
}

debug() {
    printer -setup "Starting debug..."

    # Docker
    docker builder prune -f
    docker compose down --volumes
    docker compose up --build
    handler
}

setup() {

    # Docker
    printer -setup "Setting up Docker resources..."
    docker compose down --volumes --rmi all
    docker builder prune -f
    docker compose up --build
    handler
}

clean() {

    # Docker
    printer -clean "Cleaning Docker resources..."
    docker compose down --volumes --rmi all
    handler
}

usage() {
    cat <<EOF

1. Usage:
    - bash $0 <command> [options]

2. Commands:
    - [${ICON_START}] start
    - [${ICON_STOP}] stop
    - [${ICON_SETUP}] setup
    - [${ICON_SETUP}] debug
    - [${ICON_CLEAN}] clean

EOF
    exit 1
}

printer() {
    local STATUS="$1"
    local MESSAGE="$2"
    local ICON=""
    local COLOR=""
    case "$STATUS" in
        -start)
            ICON="$ICON_START"
            COLOR="$BLUE"
            ;;
        -stop)
            ICON="$ICON_STOP"
            COLOR="$RED"
            ;;
        -debug)
            ICON="$ICON_RUN"
            COLOR="$CYAN"
            ;;
        -setup)
            ICON="$ICON_SETUP"
            COLOR="$MAGENTA"
            ;;
        -install)
            ICON="$ICON_SETUP"
            COLOR="$MAGENTA"
            ;;
        -clean)
            ICON="$ICON_CLEAN"
            COLOR="$YELLOW"
            ;;
        -success)
            ICON="$ICON_OK"
            COLOR="$GREEN"
            ;;
        -error)
            ICON="$ICON_ERR"
            COLOR="$RED"
            ;;
        *)
            ICON="ICON_ERR"
            COLOR="$RED"
            ;;
    esac
    echo ""
    printf "%b%s %s%b\n" "$COLOR" ["$ICON"] "$MESSAGE" "$RESET"
    echo ""
}

handler() {
    if [ $? -eq 0 ]; then
        printer -success "Process completed successfully"
    else
        printer -error "An unexpected error occurred"
        exit 1
    fi
}

case $1 in
    start)
        start
        ;;
    stop)
        stop
        ;;
    setup)
        setup
        ;;
    debug)
        debug
        ;;
    clean)
        clean
        ;;
    *)
        usage
        ;;
esac
