FROM python:3.8.3-slim

# Project file structure.
RUN mkdir -p /opt/app/api /opt/app/config/

# Requirements.
COPY requirements.txt /opt/app
RUN pip install -r /opt/app/requirements.txt

ARG ENVIRONMENT

# Source code.
COPY api /opt/app/api
COPY deployment/configs/gunicorn.$ENVIRONMENT.py /opt/app/config/gunicorn_conf.py

# Run.
ENV PYTHONPATH /opt/app
WORKDIR /opt/app

CMD ["gunicorn", "--reload", "-k", "gevent", "-c", "/opt/app/config/gunicorn_conf.py", "api:create_app()"]
