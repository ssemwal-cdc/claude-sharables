#!/bin/sh
# PreToolUse hook for Bash. Refuses the commands the global mandate forbids in a
# shared checkout, before they run.
#
#   git stash | git reset | git restore      each can discard another agent's work
#   git checkout -- <path> | git checkout <existing path>   the same, per path
#   pkill -f | lsof -t                       both act machine-wide, across sessions
#
# A bare branch name is allowed: `git checkout main` and `git checkout -b x` move this
# worktree only. Contract: read the tool input JSON on stdin, exit 2 with one line on
# stderr to refuse, exit 0 to allow. The reason names the refused command. It never
# names a way to reach the same target.
#
# Test it by hand:
#   echo '{"tool_input":{"command":"git reset --hard"}}' | sh scripts/refuse_shared_tree.sh
#
# POSIX sh. jq is used when present, a sed fallback when it is not.

set -f  # no globbing while the command is split into words

input=$(cat)

if command -v jq >/dev/null 2>&1; then
    cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // .command // empty' 2>/dev/null)
else
    # One JSON string value, unescaped enough for word matching.
    cmd=$(printf '%s' "$input" | tr '\n' ' ' |
        sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\(\([^"\\]\|\\.\)*\)".*/\1/p' |
        sed -e 's/\\n/ /g' -e 's/\\t/ /g' -e 's/\\"/"/g' -e 's/\\\\/\\/g')
fi

[ -z "$cmd" ] && exit 0

# Drop the quote characters, so `bash -c "git reset --hard"` still reads as git reset.
cmd=$(printf '%s' "$cmd" | tr -d '"'"'")

refuse() {
    printf 'Refused: %s. %s\n' "$1" "$2" >&2
    exit 2
}

# Split on the shell separators, so a forbidden command cannot hide behind && or ;.
segments=$(printf '%s' "$cmd" | tr ';|&\n' '\n\n\n\n')

OLDIFS=$IFS
IFS='
'
for segment in $segments; do
    IFS=$OLDIFS
    set -- $segment
    [ $# -eq 0 ] && { IFS='
'; continue; }

    # Drop leading env assignments and wrappers, so `sudo git reset` and
    # `bash -c git reset` are both still seen.
    while [ $# -gt 0 ]; do
        case "$1" in
            *=*) shift ;;
            sudo|command|time|nice|exec|env) shift ;;
            sh|bash|zsh|dash|ksh|/bin/sh|/bin/bash) shift ;;
            -c|-lc|-cl|-ec|-xc) shift ;;
            *) break ;;
        esac
    done
    [ $# -eq 0 ] && { IFS='
'; continue; }

    tool=${1##*/}
    shift

    case "$tool" in
    git)
        # Skip git's own global options, so `git -C dir reset` is still seen.
        while [ $# -gt 0 ]; do
            case "$1" in
                -C|-c|--git-dir|--work-tree|--namespace) shift; [ $# -gt 0 ] && shift ;;
                --git-dir=*|--work-tree=*|--namespace=*|-p|--paginate|--no-pager|--bare) shift ;;
                *) break ;;
            esac
        done
        [ $# -eq 0 ] && { IFS='
'; continue; }
        sub=$1
        shift
        case "$sub" in
        stash)
            refuse "git stash in a shared checkout" "The stash stack is shared, so a push or a pop can move work another session owns." ;;
        reset)
            refuse "git reset in a shared checkout" "It rewrites the index and can throw away uncommitted work another session owns." ;;
        restore)
            refuse "git restore in a shared checkout" "It overwrites a working file and can throw away uncommitted work another session owns." ;;
        checkout)
            for arg in "$@"; do
                case "$arg" in
                --)
                    refuse "git checkout with a path in a shared checkout" "It overwrites a working file and can throw away uncommitted work another session owns." ;;
                -*)
                    continue ;;
                *)
                    if [ -e "$arg" ]; then
                        refuse "git checkout of the existing path $arg in a shared checkout" "It overwrites a working file and can throw away uncommitted work another session owns."
                    fi
                    ;;
                esac
            done
            ;;
        esac
        ;;
    pkill)
        for arg in "$@"; do
            case "$arg" in
            -f|-f*)
                refuse "pkill -f" "The pattern is matched machine-wide, so it can kill a process another session or another person started." ;;
            esac
        done
        ;;
    lsof)
        for arg in "$@"; do
            case "$arg" in
            -t|-t*)
                refuse "lsof -t" "The pid list is machine-wide, and it is read to act on a process another session or another person started." ;;
            esac
        done
        ;;
    esac
    IFS='
'
done
IFS=$OLDIFS

exit 0
