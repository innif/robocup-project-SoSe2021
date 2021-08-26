FROM ubuntu:16.04

RUN apt-get update && apt-get upgrade -y && apt-get install -y python2.7 wget \
        && mkdir /opt/naoqi

WORKDIR /opt/naoqi

RUN wget -nv https://community-static.aldebaran.com/resources/2.8.6/pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327.tar.gz \
        && tar -xf pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327.tar.gz \
        && rm pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327.tar.gz

COPY naoqi_run.py .

ENV PYTHONPATH="/opt/naoqi/pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327/lib/python2.7/site-packages:${PYTHON_PATH}"
ENV QI_SDK_PREFIX="/opt/naoqi/pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327"

EXPOSE 8000

CMD ["python2.7", "naoqi_run.py", "--naoip", "172.17.0.1"]
