#!/bin/bash

# =========================
# Configurations
# =========================

# Icons
ICON_START="▶"     # U+25B6
ICON_STOP="■"      # U+25A0
ICON_SETUP="⚙"     # U+2699
ICON_DOWNLOAD="↓"  # U+2193
ICON_CLEAN="♻"     # U+267B
ICON_OK="✓"        # U+2713
ICON_ERR="✗"       # U+2717

# Colors
RESET="\033[0m"
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
MAGENTA="\033[35m"
CYAN="\033[36m"

# =========================
# Methods
# =========================

start() {
    printer -start "Starting the project..."

    # Docker
    docker compose start

    # Handler
    STATUS=$?
    handler $STATUS
}

stop() {
    printer -stop "Stopping the project..."

    # Docker
    docker compose stop

    # Handler
    STATUS=$?
    handler $STATUS
}

debug() {
    printer -setup "Debugging the project..."

    # Docker
    docker builder prune -f
    docker compose down --volumes
    docker compose up --build

    # Handler
    STATUS=$?
    handler $STATUS
}

setup() {

    # Docker
    printer -setup "Setting up the project..."
    docker compose down --volumes --rmi all
    docker builder prune -f
    docker compose up --build

    # Handler
    STATUS=$?
    handler $STATUS
}

clean() {

    # Docker
    printer -clean "Cleaning the project resources..."
    docker compose down --volumes --rmi all

    # Handler
    STATUS=$?
    handler $STATUS
}

# =========================
# Handlers
# =========================

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
            ICON="$ICON_START"
            COLOR="$CYAN"
            ;;
        -setup)
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
            ICON="$ICON_ERR"
            COLOR="$RED"
            ;;
    esac
    echo ""
    echo -e "${COLOR}[${ICON}] ${MESSAGE}${RESET}"
    echo ""
}

handler() {
    local STATUS=$1
    if [ $STATUS -eq 0 ]; then
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
