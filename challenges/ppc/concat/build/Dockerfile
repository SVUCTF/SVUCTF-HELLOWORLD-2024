FROM alpine:latest AS builder

COPY src /app/src
WORKDIR /app
RUN apk add racket fontconfig-dev cairo-dev jpeg-dev pango-dev --no-cache && \
    raco pkg install --auto --no-docs brag && \
    raco exe --orig-exe -o challenge src/main.rkt

FROM ghcr.io/svuctf/base-v2/xinetd:latest

RUN apk add ncurses lz4-libs --no-cache

COPY --from=builder /app/challenge /challenge
COPY xinetd.conf /etc/xinetd.conf

CMD ["xinetd", "-dontfork"]
