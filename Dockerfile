FROM python:3.9
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less libboost-dev swig build-essential cmake git
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install scikit-build matplotlib scipy numpy
RUN git clone https://github.com/dwavesystems/dwave-tabu.git
WORKDIR /dwave-tabu
RUN pip install -r requirements.txt
RUN python3 setup.py build_ext --inplace
RUN python3 setup.py install
RUN pip install dwave-ocean-sdk --ignore-installed
#RUN dwave setup --install-all -y