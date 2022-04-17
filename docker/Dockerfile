FROM ubuntu:focal

# Install base packages
RUN set -ex \
    \
    && cp /etc/apt/sources.list /etc/apt/sources.list.bak \
    && sed -i 's@archive.ubuntu.com@mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list \
    && sed -i 's@ports.ubuntu.com@mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list \
    && apt update \
    && apt install -y bash gzip tar wget \
    # && rm -rf /var/lib/apt/lists/* \
    # && mv /etc/apt/sources.list.bak /etc/apt/sources.list \
    # && pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple \
    # && python3 -m pip install -U pip setuptools wheel \
    && apt clean \
    && rm -rf /root/.cache/* || echo "No cache in .cache" \
    && rm -rf /var/cache/* || echo "No cache in /var" \
    && rm -rf /var/lib/apt/lists/* || echo "No apt lists"
    # && rm -rf /root/.config/pip

# Install firefox
RUN set -ex \
    \
    && apt update \
    && apt install -y firefox firefox-geckodriver firefox-locale-zh-hans firefox-locale-zh-hant firefox-locale-ja firefox-locale-ko \
    && apt install -y fonts-noto-core fonts-noto-cjk fonts-noto-color-emoji language-pack-zh-hans language-pack-zh-hant language-pack-ja language-pack-ko \
    && apt clean \
    && rm -rf /root/.cache/* || echo "No cache in .cache" \
    && rm -rf /var/cache/* || echo "No cache in /var" \
    && rm -rf /var/lib/apt/lists/* || echo "No apt lists"

# Adjust font preferences
COPY 64-language-selector-prefer.conf /etc/fonts/conf.d/64-language-selector-prefer.conf

# Install conda
RUN set -ex \
    \
    && wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh -O /tmp/install-conda.sh \
    && bash /tmp/install-conda.sh -b -p /opt/conda \
    && export CONDA_EXE=/opt/conda/bin/conda \
    && $CONDA_EXE init bash \
    && source /root/.bashrc > /dev/null \
    && $CONDA_EXE config --set show_channel_urls false \
    && rm -rf /tmp/install-conda.sh \
    && rm -rf /root/.cache/* || echo "No cache in .cache"

# Create conda environment
RUN set -ex \
    \
    && export CONDA_EXE=/opt/conda/bin/conda \
    && $CONDA_EXE create -n tg python=3.9 pip setuptools wheel flask requests gunicorn selenium python-telegram-bot -y \
    && conda activate tg > /dev/null \
    && export CONDA_TG=/opt/conda/envs/tg/bin/python3 \
    && $CONDA_TG -m pip install -U python-telegram-bot \
    && rm -rf /root/.cache/* || echo "No cache in .cache"

# Download repo
# No, I'll use volume mount
# RUN set -ex \
#     \
#     && wget https://github.com/KumaTea/KumaTea-bot/tarball/master -O /tmp/tg-bot.tar.gz \
#     && tar -xvzf /tmp/tg-bot.tar.gz -C /root/TGBot \
#     && rm -rf /tmp/tg-bot.tar.gz \

# Set entrypoint
ENTRYPOINT ["/bin/bash", "/home/kuma/bots/TGBot/run-docker.sh"]
