#!/bin/bash

DRY="0"
TEST="0"

RUN=""
#echo "0:$0 1:$1 2:$2 3:$3 4:$4"
if [ "$1" == "-l" ]; then
    RUN="python3 -m pip install -e ."
elif [ "$1" == "-b" ]; then
    RUN="python3 -m build"
elif [ "$1" == "-u" ]; then
    if [ "$TEST" == "1" ]; then
        RUN="python3 -m twine upload -r testpypi dist/*"
    else
        RUN="python3 -m twine upload dist/*"
    fi
elif [ "$1" == "-v" ]; then
    CMD="bumpver update"
    if [ "$2" == "-p" ]; then
        CMD="${CMD} --patch"
    elif [ "$2" == "-m" ]; then
        CMD="${CMD} --minor"
    elif [ "$2" == "-M" ]; then
        CMD="${CMD} --major"
    else
        exit
    fi
    if [ "$DRY" == "1" ]; then
        CMD="${CMD} --dry -n"
    fi
    RUN="${CMD}"
fi

#echo "Checking run:"
if [[ ! -z $RUN ]]; then
    echo "Running: $RUN"
    $RUN
fi
exit
