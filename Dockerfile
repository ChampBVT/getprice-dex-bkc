# use python container image
FROM python:3.9.5-slim

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

# set the working directory of the image filesystem
WORKDIR /src

RUN groupadd -r python && useradd -m -r -g python python

# Install the python dependencies
COPY --chown=python:python Pipfile Pipfile.lock /src/

RUN pip install dumb-init==1.2.5 pipenv==2021.5.29

# Generate requirements file for pip to install dependencies
RUN pipenv lock --keep-outdated --requirements > requirements.txt

RUN pip install -r requirements.txt

# copy current directory to the working directory
COPY --chown=python:python . /src

USER python 

CMD ["dumb-init", "python", "GetPrice.py"]
