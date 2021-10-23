python install pipenv
pipenv run pip install -r requirements.txt
echo cls > start.cmd
echo pipenv run main.py >> start.cmd
start.cmd
