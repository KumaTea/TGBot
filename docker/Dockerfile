FROM kumatea/pyrogram:latest

# Create conda environment
RUN set -ex && \
    wget https://github.com/KumaTea/docker/tarball/master -O /tmp/kuma-docker.tar.gz && \
    mkdir -p /tmp/docker && \
    tar -xzf /tmp/kuma-docker.tar.gz -C /tmp/docker --strip-components 1 && \
    bash /tmp/docker/scripts/install-packages.sh "requests" "" && \
    rm -rf /tmp/docker && \
    rm /tmp/kuma-docker.tar.gz

# Download repo
# No, I'll use volume mount

# Set entrypoint
ENTRYPOINT ["/bin/bash", "/home/kuma/bots/TGBot/docker/run-docker.sh"]
