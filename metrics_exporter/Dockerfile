FROM python:2

ENV EXPORTER='exporter.py'
ENV DB_SCRIPT='db_lib.py'

COPY ${EXPORTER} ./${EXPORTER}
COPY ${DB_SCRIPT} ./${DB_SCRIPT}

RUN apt-get update && apt-get install python-mysqldb \
&& pip install mysql-connector==2.2.9 tensorflow==1.13.1

ENTRYPOINT ["python", "./exporter.py"]
