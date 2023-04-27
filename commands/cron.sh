#!/bin/sh
cd /var/www/AutodeloviShop
source venv/bin/activate

python /var/www/AutodeloviShop/commands/stock.py
python /var/www/AutodeloviShop/commands/populate.py
python /var/www/AutodeloviShop/commands/images.py
0 2 * * * source /var/www/AutodeloviShop/commands/cron.sh