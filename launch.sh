#!/bin/bash

if [ "$(uname)" = "Linux" ]; then
  echo "Linux system Detected."
  requirements_file="requirements_linux.txt"
  script_name="is_peer_loged_linux.py"
elif [ "$(uname)" = "Darwin" ]; then
    echo "MacOS system Detected ."
    requirements_file="requirements_macos.txt"
    script_name="is_peer_loged_macos.py"
else
    echo "Unsupported OS. Exiting."
    exit 1
fi

echo "creating virtual envirment..."
python3 -m venv ~/myvenv

echo "activating virtual environment..."
source ~/myvenv/bin/activate

echo "upgrading pip..."
python3 -m pip install --upgrade pip 2>/dev/null > /dev/null

echo "installing dependencies..."
pip install -r $requirements_file 2>/dev/null > /dev/null

python3 $script_name $1 $2