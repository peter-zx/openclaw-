#!/bin/bash
# VSCode Git credential helper

if [ "$1" = "Username" ]; then
    echo "peter-zx"
elif [ "$1" = "Password" ]; then
    # Try to get token from VSCode
    # This won't work without proper integration, but let's try
    echo ""
fi
