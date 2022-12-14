FROM tiangolo/meinheld-gunicorn-flask:python3.9

WORKDIR /app

ADD . /app


ENV STATIC_URL /static
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
ENV NAME DOCKER
EXPOSE 80
COPY requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["gunicorn", "--conf", "/app/gunicorn_conf.py", "--bind", "0.0.0.0:80", "main:app"]