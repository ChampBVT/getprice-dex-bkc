# use python container image
FROM python:3.9.5-alpine as builder

# set the working directory of the image filesystem
WORKDIR /service

RUN pip install pipenv==2021.5.29

COPY Pipfile Pipfile.lock /service/

# Generate requirements file for pip to install dependencies
RUN pipenv lock --keep-outdated --requirements > requirements.txt

COPY . /service

#####################################################################

FROM python:3.9.5-slim as development

WORKDIR /service

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN groupadd -r python && useradd -m -r -g python python

COPY --from=builder --chown=python:python /service .

RUN pip install dumb-init==1.2.5

RUN pip install -r requirements.txt

WORKDIR /service/src

USER python

EXPOSE 8000

CMD ["dumb-init", "uvicorn", "--host", "0.0.0.0", "main:app", "--reload"]

##############################################################################

FROM python:3.9.5-slim as deployment

WORKDIR /service

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN groupadd -r python && useradd -m -r -g python python

COPY --from=builder --chown=python:python /service .

RUN pip install dumb-init==1.2.5

RUN pip install -r requirements.txt

WORKDIR /service/src

USER python

EXPOSE 80

CMD ["dumb-init", "uvicorn", "--host", "0.0.0.0", "main:app", "--port", "80"]