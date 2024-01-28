:; python3 -m venv pyenv
:; echo "clear && cd $(pwd) && ./pyenv/bin/python3 main.py" > start.sh
:; chmod +x start.sh
:; ./pyenv/bin/pip3 install -r requirements.txt
:; #./start.sh
:;exit $?
@echo off
python -m venv pyenv
pyenv\Scripts\activate & pip install -r "requirements.txt" & echo cls ^& pyenv\Scripts\activate ^& python main.py > start.bat
