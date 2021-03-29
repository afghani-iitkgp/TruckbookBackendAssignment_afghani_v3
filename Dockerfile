FROM ubuntu:18.04
LABEL "afghaniiit@gmail.com"
# RUN apk add --no-cache python3 openssl ca-certificates git openssh sshpass \
#     && apk --update add --virtual build-dependencies python3-dev libffi-dev openssl-dev build-base \
#     && pip3 install --upgrade pip cffi


RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y python3-pip \
    && apt-get install -y python3.7 \
#     && apt install -y python3 \
    && apt install python3-venv -y \
    && python3 -m venv venv \
    && pip3 install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /docker_app
COPY . /docker_app

RUN pip3 --no-cache-dir install -r ./Configuration/requirements.txt

EXPOSE 5011

ENTRYPOINT ["python3"]
CMD ["run_flasked_app.py"]