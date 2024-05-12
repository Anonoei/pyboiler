#!/bin/bash

PY_EXE="python3"
DRY="1"
DOCS="0"

cd "$(git rev-parse --show-toplevel)"

cmd_help() {
    echo "pyboiler build helpers"
    echo
    echo "./build.sh [-l|b|u|t|f|d|p|v [-M|m|p]] [-r]"
    echo "Commands"
    echo "  -l|--local    Install pyboiler locally"
    echo "  -b|--build    Build pyboiler for uploading"
    echo "  -u|--upload   Upload pyboiler"
    echo "  -t|--test    Run pytest"
    echo "  -f|--format   Run black formatter"
    echo "  -d|--docs     Make documentation"
    echo "  -p|--prepare  Run format, test, and docs"
    echo "  -v|--version  Bump version"
    echo "   -M|--major     Bump #.X.X"
    echo "   -m|--minor     Bump X.#.X"
    echo "   -p|--patch     Bump X.X.#"
    echo "options"
    echo "  -r  actually run the commands and upload"
}

cmd_exec() {
    echo "Running \"$1\""
    $1
}

cmd_local() {
    cmd_exec "$PY_EXE -m pip install -e ."
}
cmd_build() {
    cmd_exec "rm dist/*"
    cmd_exec "$PY_EXE -m build"
}
cmd_update() {
    if [ "$DRY" == "0" ]; then
        cmd_exec "$PY_EXE -m twine upload dist/*"
    else
        cmd_exec "$PY_EXE -m twine upload -r testpypi dist/*"
    fi
}
cmd_test() {
    cmd_exec "pytest"
}
cmd_format() {
    cmd_exec "black src/pyboiler"
}
cmd_version() {
    bump="bumpver update"
    if [ "$DRY" == "1" ]; then
        bump="$bump --dry -n"
    fi
    if [[ "$1" == "-M" || "$1" == "--major" ]]; then
        bump="$bump --major"
    elif [[ "$1" == "-m" || "$1" == "--minor" ]]; then
        bump="$bump --minor"
    elif [[ "$1" == "-p" || "$1" == "--patch" ]]; then
        bump="$bump --patch"
    else
        echo "-v|--version requires a second argument!"
        exit
    fi
    cmd_exec "$bump"
}
cmd_docs() {
    cmd_exec "python3 -m pdoc -o docs --html src/pyboiler --force"
    cmd_exec "mv docs/pyboiler/* docs/"
    cmd_exec "rm -r docs/pyboiler"
}
cmd_prepare() {
    cmd_format
    cmd_test
    cmd_docs
}

if [ $# -eq 0 ]; then
    cmd_help
    exit
fi

if [[ $* == *"-r"* ]]; then
    DRY="0"
fi

cmd=$1
case $cmd in
  "-l"|"--local")
    cmd_local ;;
  "-b"|"--build")
    cmd_build ;;
  "-u"|"--upload")
    cmd_update ;;
  "-t"|"--test")
    cmd_test ;;
  "-f"|"--format")
    cmd_format ;;
  "-d"|"--docs")
    cmd_docs ;;
  "-v"|"--version")
    cmd_version $2 ;;
  "-p"|"--prepare")
    cmd_prepare ;;
  *)
    cmd_help
esac
