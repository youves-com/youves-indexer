FROM python:3.10
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y install --no-install-recommends python3-dev python3-pip python3-setuptools libsodium-dev libsecp256k1-dev 
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt && pip install uWSGI==2.0.20

COPY ./app.py /code/app.py

ENTRYPOINT [ "uwsgi" ]
CMD ["--http", "0.0.0.0:5000", "--wsgi-file", "app.py", "--callable", "app", "--vhost", "-T", "--processes", "4", "-M", "--logger", "stdio", "--offload-threads", "%k"]