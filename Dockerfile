FROM python:3.8

ADD app /app
RUN pip install -r /app/requirements.txt
WORKDIR /app
ENV PYTHONPATH '/app/'

# CMD kopf run -A --standalone --verbose --log-format=json /app/main.py
CMD kopf run /app/main.py
