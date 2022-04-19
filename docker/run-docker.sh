#!/usr/bin/env bash

set -ex

cd /home/kuma/bots/TGBot
/opt/conda/envs/tg/bin/gunicorn --bind=0.0.0.0:10560 main:app
