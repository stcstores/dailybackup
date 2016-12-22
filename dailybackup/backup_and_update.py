#!env/Scripts/python.exe -i


import os
import shutil

from . backup import backup
import stclocal
from stclocal import PyLinnworks
from . update import update_inventory, update_linking


def download_linking_table(linking_filename):
    print('Downloading linking file')
    linking_table = PyLinnworks.Export().get_linking_table()
    linking_table.write(os.path.join(stclocal.DOWNLOAD_DIR, linking_filename))


def move_shopify_products_from_downloads():
    print('Moving Shopify Products file from Downloads')
    download_folder = os.path.expanduser('~/Downloads')
    filename = 'products_export.zip'
    if os.path.isfile(os.path.join(download_folder, filename)):
        shutil.move(
            os.path.join(download_folder, filename),
            os.path.join(stclocal.DOWNLOAD_DIR, filename))
    else:
        raise Exception('Shopfiy Products not in Downloads')


def main():
    download_linking_table('linnworks_linking.csv')
    move_shopify_products_from_downloads()
    backup()
    update_inventory()
    update_linking()

if __name__ == "__main__":
    main()
