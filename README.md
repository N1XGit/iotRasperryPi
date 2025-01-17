# iotRasperryPi
# IoT projektirepo
https://github.com/Seeed-Studio/grove.py/tree/master
wget https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/lcd_16x2.py

wget https://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.5.11.tar.gz

##

echo "deb https://seeed-studio.github.io/pi_repo/ stretch main" | sudo tee /etc/apt/sources.list.d/seeed.list
curl https://seeed-studio.github.io/pi_repo/public.key | sudo apt-key add -
sudo raspi-config

sudo apt install python3-virtualenv
virtualenv -p python3 env
source env/bin/activate
pip install rpi-gpio
sudo pip3 install rpi_ws281x
pip install rpi_ws281x

curl -sL https://github.com/Seeed-Studio/grove.py/raw/master/install.sh | sudo bash -s -
git clone https://github.com/Seeed-Studio/grove.py
cd grove.py
sudo pip3 install .

sudo apt install python3-virtualenv
virtualenv -p python3 env
source env/bin/activate
pip3 install .
