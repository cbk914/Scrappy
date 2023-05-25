# Dockerfile
FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY scrappy-cli.py scrappy-cli.py
COPY scrappy-web.py scrappy-web.py
COPY scrappy-api.py scrappy-api.py
COPY scrappy-db.py scrape-db.py
COPY scrappy-srv.sh scrappy-srv.sh
COPY scrappy.yaml scrappy.yaml

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD [ "python", "./scrappy.cli.py" ]
CMD [ "python", "./scrappy-web.py" ]
CMD [ "python", "./scrappy-api.py" ]
CMD [ "python", "./scrappy-db.py" ]
CMD [ "python", "./scrappy-web.py" ]
CMD [ "bash", "./scrappy-srv.sh" ]