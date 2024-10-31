#!/bin/sh

mkdir /home/ctf/.hidden/
echo $GZCTF_FLAG > /home/ctf/.hidden/flag
chown -R ctf:ctf /home/ctf/.hidden/
unset GZCTF_FLAG

/usr/sbin/chroot /home/ctf/ /bin/sh
