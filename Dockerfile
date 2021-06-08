FROM python:3
WORKDIR /usr/src/

ENV FLASK_APP=cats_api.py
ENV FLASK_RUN_HOST=0.0.0.0

# Instala requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia coletor
COPY settings.py settings.py
COPY coletor.py coletor.py
RUN python coletor.py

# Copia api
COPY cats_api.py cats_api.py
RUN mkdir logs

# Run server
EXPOSE 5000
CMD ["flask", "run"]
