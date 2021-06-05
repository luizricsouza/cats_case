FROM python:3
WORKDIR /usr/src/

# Get app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY settings.py settings.py
COPY coletor.py coletor.py
RUN python coletor.py
COPY apis.py apis.py

# Run server
EXPOSE 5000
CMD python apis.py
