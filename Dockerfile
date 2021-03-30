FROM python:3.7-alpine


ENV PYTHONUNBUFFERED=1

RUN apk add build-base
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
# RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

WORKDIR /app
COPY . /app

RUN pip3 --no-cache-dir install -r ./Configuration/requirements.txt

EXPOSE 5011

ENTRYPOINT ["python3"]
CMD ["run_flasked_app.py"]
