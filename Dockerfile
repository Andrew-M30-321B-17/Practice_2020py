FROM python:latest
COPY task1/ /usr/task1/
WORKDIR /usr/
RUN apt-get update && apt-get install -y apt-utils \
    && apt-get -y install locales
RUN apt-get install -y python3-pip python-psycopg2 && pip3 install setuptools influxdb PyQt5 pyqtgraph \
    && apt-get install -y pyqt5-dev-tools
CMD ["python3", "-m", "task1.write", "&", "python3", "-m", "task1.monitor"]