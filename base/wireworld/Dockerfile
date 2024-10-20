FROM node:22-alpine AS builder

COPY frontend /app

WORKDIR /app

RUN yarn run build

FROM python:3.12-alpine

COPY app /app
COPY challenge.toml /challenge.toml

RUN pip install --no-cache-dir -r /app/requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apk add --no-cache shadow nginx && mkdir -p /run/nginx && \
    adduser -u 1000 -D -S -G www-data www-data && \
    ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --chown=www-data:www-data --from=builder /app/dist /var/www/html
COPY --chmod=500 init.sh /init.sh

CMD ["/init.sh"]
