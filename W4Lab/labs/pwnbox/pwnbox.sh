#!/usr/bin/env bash

set -euo pipefail

IMAGE=pwnbox:22.04
NAME=pwnbox-22.04
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case "${1:-}" in
    build)
        docker build -t "$IMAGE" "$HERE"
        ;;
    export)
        docker save "$IMAGE" -o "${2:-$NAME.tar}"
        ;;
    load)
        docker load -i "${2:-$NAME.tar}"
        ;;
    start)
        mkdir -p data
        docker run -dit --name "$NAME" \
            --cap-add=SYS_PTRACE --security-opt seccomp=unconfined \
            -v "$PWD/data":/work \
            "$IMAGE"
        ;;
    shell)
        docker exec -it "$NAME" fish
        ;;
    stop)
        docker rm -f "$NAME"
        ;;
    uninstall)
        docker rmi "$IMAGE"
        ;;
    *)
        echo "usage: $0 {build|export [tar]|load [tar]|start|shell|stop|uninstall}" >&2
        exit 1
        ;;
esac
