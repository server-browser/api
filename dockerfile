FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-alpine3.14

EXPOSE 80

ENV MODULE_NAME="api.app"

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./ /app
