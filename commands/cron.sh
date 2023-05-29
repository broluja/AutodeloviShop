#!/bin/sh
rm GENUINE_02850.txt OUTOFSTOCK_SRB.txt PRICELIST_02850.txt REFAR_02850.txt
unzip /home/autodelovi/ftp/OUTOFSTOCK_SRB.ZIP -A

unzip /home/autodelovi/ftp/PRICELIST_02850.ZIP

unzip /home/autodelovi/ftp/GENUINE_02850.ZIP

unzip /home/autodelovi/ftp/REFAR_02850.ZIP

cd /var/www/AutodeloviShop || exit
source venv/bin/activate
cd commands || exit

python stock.py
python populate.py
python images.py
