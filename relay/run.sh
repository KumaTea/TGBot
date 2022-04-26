set -e

cd /home/kuma/bots/TGBot/relay
/opt/conda/bin/gunicorn --bind=0.0.0.0:10561 main:app
# /opt/conda/bin/python3 main.py
