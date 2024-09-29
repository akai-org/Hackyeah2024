FROM python:3.12

# WORKDIR .
WORKDIR /app


RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt && pip install daphne

COPY . /app

CMD ["bash", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 8000 taxHackYeah.asgi:application --verbosity 2"]
