FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000

WORKDIR /app/src

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
