sudo docker start mongodb
export FLASK_APP=./flask_app/main.py
source ./flask_app/venv/bin/activate

flask run --host=0.0.0.0
