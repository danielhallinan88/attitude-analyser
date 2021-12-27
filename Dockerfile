WORKDIR nltk_data

RUN python -m nltk.downloader -d nltk_data/ all
