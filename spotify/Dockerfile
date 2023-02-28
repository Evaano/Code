FROM python:3.11.2
WORKDIR /spotify
COPY requirements.txt /spotify/
RUN pip install -r requirements.txt
COPY . /spotify
CMD python spotify.py