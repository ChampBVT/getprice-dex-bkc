# TODO Multi-stage building
# use python container image
FROM python:3.9.5-slim

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

# set the working directory of the image filesystem
WORKDIR /service

RUN groupadd -r python && useradd -m -r -g python python

# Install the python dependencies
COPY --chown=python:python Pipfile Pipfile.lock /service/

RUN pip install dumb-init==1.2.5 pipenv==2021.5.29

# Generate requirements file for pip to install dependencies
RUN pipenv lock --keep-outdated --requirements > requirements.txt

RUN pip install -r requirements.txt

# copy current directory to the working directory
COPY --chown=python:python . /service

USER python

EXPOSE 8000

WORKDIR /service/src

CMD ["dumb-init", "uvicorn", "--host", "0.0.0.0", "main:app", "--reload"]
