FROM ghcr.io/svuctf/base-v2/python-xinetd:latest

WORKDIR /app

COPY machine.py machine.py
COPY requirements.txt requirements.txt

COPY xinetd.conf /etc/xinetd.conf
COPY --chmod=500 init.sh /init.sh

RUN pip install -r requirements.txt

CMD ["xinetd", "-dontfork"]
