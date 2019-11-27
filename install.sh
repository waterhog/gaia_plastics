#!/bin/bash

echo "Installing dependencies (this may take some time)..."

sudo apt-get update

sudo apt-get install libhdf5-dev -y
sudo apt-get install libatlas-base-dev -y
sudo apt-get install libjasper-dev  -y
sudo apt-get install libqtgui4  -y
sudo apt-get install libqt4-test -y
sudo apt-get install tdsodbc -y
sudo apt-get install unixodbc-dev -y

pip3 install opencv-python==3.4.4.19
pip3 install opencv-contrib-python==3.4.4.19
pip3 install pyodbc
pip3 install pyserial

echo "Copying odbcinst.ini to /etc/..."

sudo cp /home/pi/gaia_plastics/app/conf/odbc/odbcinst.ini /etc/

echo "Setting up WiFi IP address emailing and application to run when RPI powered on..."

sudo sed -i '/^exit 0.*/i sudo python /home/pi/gaia_plastics/email_ip.py\npython3 /home/pi/gaia_plastics/app/code/main.py' /etc/rc.local

echo "Done with software setup"