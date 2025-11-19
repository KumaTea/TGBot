# prepare data/
# prepare config.ini
# prepare local_functions.py

git clone https://github.com/KumaTea/bots-share share
docker run --name=tgbot --restart=unless-stopped -v /home/kuma/bots/TGBot:/home/kuma/bots/TGBot -d kumatea/tgbot
