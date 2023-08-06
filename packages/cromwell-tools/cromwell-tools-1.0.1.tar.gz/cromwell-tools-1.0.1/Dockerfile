FROM ubuntu:16.04

LABEL maintainer = "Mint Team <mintteam@broadinstitute.org>" \
  software = "cromwell-tools" \
  description = "python package and CLI for interacting with cromwell" \
  website = "https://github.com/broadinstitute/cromwell-tools.git"

# Install required packages
RUN apt-get update && apt-get upgrade -y && apt-get -y install --no-install-recommends --fix-missing \
    python-pip \
    python3-pip \
    git

# Install java 8
ENV DEBIAN_FRONTEND noninteractive
ENV JAVA_HOME       /usr/lib/jvm/java-8-oracle
ENV LANG            en_US.UTF-8
ENV LC_ALL          en_US.UTF-8

RUN apt-get update && \
  apt-get install -y --no-install-recommends locales && \
  locale-gen en_US.UTF-8 && \
  apt-get dist-upgrade -y && \
  apt-get --purge remove openjdk* && \
  echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | debconf-set-selections && \
  echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu xenial main" > /etc/apt/sources.list.d/webupd8team-java-trusty.list && \
  apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EEA14886 && \
  apt-get update && \
  apt-get install -y --no-install-recommends oracle-java8-installer oracle-java8-set-default && \
  apt-get clean all

# Download and expose womtool
ADD https://github.com/broadinstitute/cromwell/releases/download/35/womtool-35.jar /usr/local/bin/womtool/womtool-35.jar
ENV WOMTOOL /usr/local/bin/womtool/womtool-35.jar

# Upgrade pip for Python2
RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install --upgrade setuptools

# Upgrade pip3 for Python3
RUN pip3 install -U setuptools
RUN pip3 install -U pip
RUN pip3 install wheel

# Copy the whole module
WORKDIR /cromwell-tools
COPY . .

# Install dependencies(including those for testing)
RUN pip2 install .[test]
RUN pip3 install .[test]
