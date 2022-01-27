FROM python:3.8

WORKDIR /app

COPY app.py app.py

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN python -m spacy download en_core_web_sm

RUN python -m nltk.downloader -d nltk_data/ all

#PORT 5000
EXPOSE $PORT
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]