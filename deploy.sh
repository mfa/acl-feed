#!/bin/sh

rsync -avP . madflex.de:~/caddy/acl-feed/ --exclude .git --exclude __pycache__ --exclude cache
