#!/bin/bash

set -ex

sleep 5
/usr/local/bin/cloudflared tunnel --name tg --config /home/kuma/.cloudflared/tg.yaml > /tmp/cftg.log 2>&1 &

sleep 5
cd /home/kuma/bots/TGBot
/home/kuma/.conda/envs/tg/bin/gunicorn --bind=127.0.0.1:10560 main:app
