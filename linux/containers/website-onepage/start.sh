#!/bin/sh

podman run -d -p 8888:80 --name nginx \
    -v ./html:/usr/share/nginx/html:Z,U \
    -v ./sites:/etc/nginx/conf.d:Z,U \
    nginx
