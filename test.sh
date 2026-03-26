#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./test.sh          Run all tests
#   ./test.sh cli      Run CLI tests
#   ./test.sh go       Run 'go' command tests
#   ./test.sh where    Run 'where' command tests
#   ./test.sh book     Run 'book' command tests
#
# Extra pytest flags are forwarded:
#   ./test.sh go -x --tb=short

COMMAND="${1:-}"
shift 2>/dev/null || true   # remaining args forwarded to pytest

case "$COMMAND" in
    "")    pytest tests/ "$@" ;;
    cli)   pytest tests/test_cli.py "$@" ;;
    go)    pytest tests/test_go.py "$@" ;;
    where) pytest tests/test_where.py "$@" ;;
    book)  pytest tests/test_book.py "$@" ;;
    *)
        echo "Unknown alias: $COMMAND"
        echo "Available: cli, go, where, book (or blank for all)"
        exit 1
        ;;
esac
