py -m venv python-env
python-env\Scripts\activate & pip install -r "requirements.txt" & echo "cls ^& python-env\Scripts\activate ^& python main.py" > start.bat & start.bat
