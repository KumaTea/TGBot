#!/usr/bin/env bash

set -ex

export CONDA_EXE=/opt/conda/bin/conda
$CONDA_EXE create -n tg python=3.9 pip setuptools wheel flask requests gunicorn selenium python-telegram-bot -y
conda activate tg > /dev/null

export CONDA_TG=/opt/conda/envs/tg/bin/python3
$CONDA_TG -m pip install -U python-telegram-bot

rm -rf /root/.cache/* || echo "No cache in .cache"