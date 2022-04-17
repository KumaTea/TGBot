#!/usr/bin/env bash

set -ex

wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh -O /tmp/install-conda.sh
bash /tmp/install-conda.sh -b -p /opt/conda

export CONDA_EXE=/opt/conda/bin/conda
$CONDA_EXE init bash
source /root/.bashrc > /dev/null
$CONDA_EXE config --set show_channel_urls false

rm -rf /tmp/install-conda.sh
rm -rf /root/.cache/* || echo "No cache in .cache"