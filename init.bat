:;#!/usr/share/env python3
:; python3 -m venv pyenv
:; echo cls && echo "python main.py" > start.sh
:; chmod +x start.sh
:; source pyenv/bin/activate
:; pip install -r requirements.txt
:; ./start.sh
:;exit $?
@echo off
python -m venv pyenv
pyenv\Scripts\activate & pip install -r "requirements.txt" & echo cls ^& pyenv\Scripts\activate ^& python main.py > start.bat
