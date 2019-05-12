FROM python:2

COPY *.py db_writer.py
COPY requirements.txt .

RUN apt-get update && apt-get install python-mysqldb \
&& pip install -r requirements.txt

CMD ["python", "./db_writer.py"]
