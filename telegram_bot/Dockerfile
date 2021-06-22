# use python container image
FROM python:3.9.5-alpine as builder

# set the working directory of the image filesystem
WORKDIR /telegram_bot

RUN pip install pipenv==2021.5.29

COPY Pipfile Pipfile.lock /telegram_bot/

# Generate requirements file for pip to install dependencies
RUN pipenv lock --keep-outdated --requirements > requirements.txt

COPY . /telegram_bot

#####################################################################

FROM python:3.9.5-alpine as development

WORKDIR /telegram_bot

RUN addgroup -S python && adduser -S python -G python

RUN apk add dumb-init

COPY --from=builder --chown=python:python /telegram_bot .

RUN pip install -U py-mon==1.1.0 colorama==0.4.4 watchdog==2.1.2

RUN pip install -r requirements.txt

USER python

CMD ["dumb-init", "pymon", "main.py"]

##############################################################################

FROM python:3.9.5-alpine as production

WORKDIR /telegram_bot

RUN addgroup -S python && adduser -S python -G python

RUN apk add dumb-init

COPY --from=builder --chown=python:python /telegram_bot .

RUN pip install -r requirements.txt

WORKDIR /telegram_bot

USER python

CMD ["dumb-init", "python", "main.py"]