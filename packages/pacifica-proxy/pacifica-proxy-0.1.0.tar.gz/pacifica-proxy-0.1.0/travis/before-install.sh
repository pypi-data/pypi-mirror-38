#!/bin/bash -xe

psql -c 'create database pacifica_metadata;' -U postgres
if [ "$RUN_LINTS" = "true" ]; then
  pip install pre-commit
else
  sed -e "s|@@ROOT_DIR@@|$PWD|g;s|@@CONF_DIR@@|/etc/nginx|g" < travis/nginx.conf.in > travis/nginx.conf
  nginx -c $PWD/travis/nginx.conf &
  echo $! > nginx.pid
fi
