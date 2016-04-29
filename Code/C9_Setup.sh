#!/bin/bash

echo "Beginning setup of your Cloud 9 Workspace"

echo "Installing pip, Python3's package manager"
sudo easy_install3 pip

echo "Installing getch"
sudo python3 -m pip install getch

echo "Installing termcolor"
sudo python3 -m pip install termcolor
