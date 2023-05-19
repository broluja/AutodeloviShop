#!/bin/sh
cd /var/www/AutodeloviShop
source venv/bin/activate
cd commands

python stock.py
python populate.py
python images.py
