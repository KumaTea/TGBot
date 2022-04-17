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
    && wget https://github.com/KumaTea/KumaTea-bot/tarball/master -O /tmp/tgbot.tar.gz \
    && mkdir -p /tmp/TGBot \
    && tar -xzf /tmp/tgbot.tar.gz -C /tmp/TGBot --strip-components 1 \
    && bash /tmp/TGBot/docker/install-conda.sh \
    && rm -rf /tmp/TGBot \
    && rm /tmp/tgbot.tar.gz

# Create conda environment
RUN set -ex \
    \
    && wget https://github.com/KumaTea/KumaTea-bot/tarball/master -O /tmp/tgbot.tar.gz \
    && mkdir -p /tmp/TGBot \
    && tar -xzf /tmp/tgbot.tar.gz -C /tmp/TGBot --strip-components 1 \
    && bash /tmp/TGBot/docker/create-env.sh \
    && rm -rf /tmp/TGBot \
    && rm /tmp/tgbot.tar.gz

# Download repo
# No, I'll use volume mount
# RUN set -ex \
#     \
#     && wget https://github.com/KumaTea/KumaTea-bot/tarball/master -O /tmp/tg-bot.tar.gz \
#     && tar -xvzf /tmp/tg-bot.tar.gz -C /root/TGBot \
#     && rm -rf /tmp/tg-bot.tar.gz \

# Set entrypoint
ENTRYPOINT ["/bin/bash", "/home/kuma/bots/TGBot/docker/run-docker.sh"]
