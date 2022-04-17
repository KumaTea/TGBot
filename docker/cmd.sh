# cd docker
# cp Dockerfile local.Dockerfile; sed -i 's@bash /tmp/TGBot/docker/install-conda.sh@sed -i \'s艾特https://github.com/conda-forge/miniforge/releases/latest/download/艾特http://192.168.2.225:8080/艾特g\' /tmp/TGBot/docker/install-conda.sh \&\& bash /tmp/TGBot/docker/install-conda.sh@g' local.Dockerfile; sed -i 's/艾特/@/g' local.Dockerfile

docker run --name=tg --restart=unless-stopped -v /home/kuma/bots/TGBot:/root/TGBot -v /home/kuma/data/firefox:/home/kuma/data/firefox -p 10560:10560 -d kumatea/tgbot
