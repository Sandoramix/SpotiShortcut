pip install pipenv
pipenv run pip install -r requirements.txt

echo cls > start.bat
echo pipenv run main.py >> start.bat
start.bat
