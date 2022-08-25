FROM python:3.10-buster
# RUN pip install poetry
WORKDIR /code
# COPY poetry.lock pyproject.toml /code/
# RUN poetry config virtualenvs.create false && poetry install --no-dev
COPY . /code

# Install postgres version 13. This is a workaround for the moment because we
# need python 3.10 for dipdup and postgres 13 for the backups.

RUN bash -c 'echo "deb http://apt.postgresql.org/pub/repos/apt buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt update
RUN apt -y install postgresql-13
RUN curl -L https://github.com/odise/go-cron/releases/download/v0.0.7/go-cron-linux.gz | zcat > /usr/local/bin/go-cron && chmod +x /usr/local/bin/go-cron

RUN pip install -r requirements.txt
# ENTRYPOINT ["dipdup"]
CMD ["dipdup", "-c", "config.yml", "run"]