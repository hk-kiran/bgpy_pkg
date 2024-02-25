FROM ubuntu
ENV DEBIAN_FRONTEND noninteractive

RUN apt update && \
    apt -y install gcc mono-mcs
RUN apt install -y build-essential
RUN apt install -y g++
RUN apt install -y wget
RUN apt install -y git
RUN apt install -y bzip2
RUN apt-get install -y graphviz libjpeg-dev zlib1g-dev  

RUN wget https://downloads.python.org/pypy/pypy3.10-v7.3.15-linux64.tar.bz2
RUN bzip2 -d pypy3.10-v7.3.15-linux64.tar.bz2
RUN tar -xf pypy3.10-v7.3.15-linux64.tar
ENV PATH="${PATH}:/pypy3.10-v7.3.15-linux64/bin"
RUN rm pypy3.10-v7.3.15-linux64.tar

RUN pypy3 -m ensurepip
RUN pypy3 -mpip install -U pip wheel
RUN pypy3 -m pip install pip --upgrade
RUN pypy3 -m pip install wheel --upgrade
RUN pypy3 -m pip install numpy --config-settings=setup-args="-Dallow-noblas=true"


RUN git clone https://github.com/hk-kiran/bgpy_pkg.git
WORKDIR /bgpy_pkg
RUN export SETUPTOOLS_ENABLE_FEATURES="legacy-editable"
RUN pypy3 -m pip install -e .[test]
RUN pre-commit install

CMD ["sleep", "infinity"]
