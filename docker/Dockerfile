FROM kumatea/tg:latest

# Install firefox
RUN set -ex && \
    apt update && \
    apt install -y firefox firefox-geckodriver firefox-locale-zh-hans firefox-locale-zh-hant firefox-locale-ja firefox-locale-ko && \
    apt install -y fonts-noto-core fonts-noto-cjk fonts-noto-color-emoji language-pack-zh-hans language-pack-zh-hant language-pack-ja language-pack-ko && \
    apt clean && \
    rm -rf /root/.cache/* || echo "No cache in .cache" && \
    rm -rf /var/cache/* || echo "No cache in /var" && \
    rm -rf /var/lib/apt/lists/* || echo "No apt lists"

# Adjust font preferences
COPY 64-language-selector-prefer.conf /etc/fonts/conf.d/64-language-selector-prefer.conf

# Create conda environment
RUN set -ex && \
    wget https://github.com/KumaTea/docker/tarball/master -O /tmp/kuma-docker.tar.gz && \
    mkdir -p /tmp/docker && \
    tar -xzf /tmp/kuma-docker.tar.gz -C /tmp/docker --strip-components 1 && \
    bash /tmp/docker/scripts/install-packages.sh "flask requests gunicorn selenium" "python-telegram-bot" && \
    rm -rf /tmp/docker && \
    rm /tmp/kuma-docker.tar.gz

# Download repo
# No, I'll use volume mount

# Set entrypoint
ENTRYPOINT ["/bin/bash", "/home/kuma/bots/TGBot/docker/run-docker.sh"]
