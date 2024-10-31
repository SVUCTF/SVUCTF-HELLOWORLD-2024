FROM ghcr.io/svuctf/base-v2/xinetd:latest

# Copy initialization script and xinetd configuration
COPY --chmod=500 init.sh /init.sh
COPY xinetd.conf /etc/xinetd.conf

# Set up the CTF environment
RUN chmod -R 750 /home/ctf && \
    mkdir -p /home/ctf/lib64 && \
    mkdir -p /home/ctf/dev && \
    mkdir -p /home/ctf/bin && \
    mkdir -p /home/ctf/lib/x86_64-linux-gnu && \
    mkdir -p /home/ctf/lib32

# Set up device nodes
RUN mknod /home/ctf/dev/null c 1 3 && \
    mknod /home/ctf/dev/zero c 1 5 && \
    mknod /home/ctf/dev/random c 1 8 && \
    mknod /home/ctf/dev/urandom c 1 9 && \
    chmod 666 /home/ctf/dev/*

# Copy necessary binaries abd binaries
RUN cp /lib/ld-musl-x86_64.so.1 /home/ctf/lib/ && \
    cp /bin/sh /home/ctf/bin && \
    cp /bin/ls /home/ctf/bin && \
    cp /bin/cat /home/ctf/bin && \
    cp /bin/base64 /home/ctf/bin 

RUN chown -R ctf:ctf /home/ctf 

CMD ["xinetd", "-dontfork"]
