FROM python:3.8-slim-buster

WORKDIR /app

COPY app.py app.py
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

#RUN python -m nltk.downloader -d nltk_data/ all

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0:5000"]
