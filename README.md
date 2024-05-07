VCLTHO001 - Graphics Practical 1

Setup assumes that you are using a Windows-based OS with python3 and python3-venv installed.

First make a virtual environment to install all dependencies:
python -m venv venv
or
python3 -m venv venv

To activate the virtual environment try:
venv/Scripts/activate.ps1
If this does not work try
. venv/bin/activate

To ensure all packages are installed please run:
pip3 install -Ur requirements.txt
pip3 install -Ur post_requirements.txt

Note: You can also put any packages you want to use in the requirements.txt file.

To run the skeleton code:

```
> python ./src/main.py
```

A pygame window should pop up and display the animation. Here are the controls:
Q = Quit Window
P = Pause/Unpause
Up/Down Arrow = Speed up/Slow down Earth
Right/Left Arrow = Speed up/Slow down Moon
