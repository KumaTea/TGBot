#!/usr/bin/env bash

set -ex

cd /root/TGBot
/opt/conda/envs/tg/bin/gunicorn --bind=127.0.0.1:10560 main:app
