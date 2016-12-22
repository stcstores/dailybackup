import os
import datetime
import shutil
from zipfile import ZipFile

from lsftp import FTP_Connection
import stclocal

DOWNLOAD_DIR = stclocal.DOWNLOAD_DIR
IMPORT_DIR = stclocal.IMPORT_DIR
INVENTORY_FILE_NAME = stclocal.INVENTORY_FILE_NAME
LINKING_FILE_NAME = stclocal.LINKING_FILE_NAME
SHOPIFY_PRODUCT_FILE_NAME = stclocal.SHOPIFY_PRODUCT_FILE_NAME
SHOPIFY_THEME_FILE_NAME = stclocal.SHOPIFY_THEME_FILE_NAME
BACKUP_DIRS = stclocal.BACKUP_DIRS


def get_date_string():
    now = datetime.datetime.now()
    day = str(now.day).zfill(2)
    month = str(now.month).zfill(2)
    year = str(now.year)
    date_string = year + '-' + month + '-' + day
    return date_string


def backup_file(filename, date_string):
    save_filename = date_string + '_' + filename
    if os.path.exists(os.path.join(DOWNLOAD_DIR, filename)):
        shutil.copyfile(
            os.path.join(DOWNLOAD_DIR, filename),
            os.path.join(IMPORT_DIR, filename))
        print('Copied ' + filename + ' to import')
        for backup_dir in BACKUP_DIRS:
            shutil.copyfile(
                os.path.join(DOWNLOAD_DIR, filename),
                os.path.join(backup_dir, date_string, save_filename))
            print('Copied ' + filename + ' to ' + backup_dir)
    else:
        print(filename + ' is missing')


def unzip(filename, date_string):
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    save_filename = date_string + '_' + filename
    for backup_dir in BACKUP_DIRS:
        if os.path.exists(filepath):
            ZipFile(filepath).extractall(
                os.path.join(
                    backup_dir, date_string, save_filename))
            print('Unzipped ' + filename + ' to ' + backup_dir)
        else:
            print(filename + ' is missing')


def backup():
    date_string = get_date_string()

    for backup_dir in BACKUP_DIRS:
        if not os.path.isdir(backup_dir):
            os.mkdir(backup_dir)
        if not os.path.isdir(os.path.join(backup_dir, date_string)):
            os.mkdir(os.path.join(backup_dir, date_string))
    backup_file(INVENTORY_FILE_NAME, date_string)
    backup_file(LINKING_FILE_NAME, date_string)
    unzip(SHOPIFY_PRODUCT_FILE_NAME, date_string)
    unzip(SHOPIFY_THEME_FILE_NAME, date_string)

    for ftp_backup in stclocal.FTP_BACKUPS:
        ftp = FTP_Connection(
            ftp_backup.host, username=ftp_backup.user,
            password=ftp_backup.password, folder=ftp_backup.path)

        ftp.mkdir(date_string)
        ftp.cd(date_string)
        print(' '.join([
            'Uploading', INVENTORY_FILE_NAME, 'to', str(ftp_backup)]))
        ftp.upload(os.path.join(DOWNLOAD_DIR, INVENTORY_FILE_NAME))
        print(' '.join(
            ['Uploading', LINKING_FILE_NAME, 'to', str(ftp_backup)]))
        ftp.upload(os.path.join(DOWNLOAD_DIR, LINKING_FILE_NAME))
        print(' '.join([
            'Uploading', SHOPIFY_PRODUCT_FILE_NAME, 'to', str(ftp_backup)]))
        ftp.upload(os.path.join(DOWNLOAD_DIR, SHOPIFY_PRODUCT_FILE_NAME))
        print(' '.join([
            'Uploading', SHOPIFY_THEME_FILE_NAME, 'to', str(ftp_backup)]))
        ftp.upload(os.path.join(DOWNLOAD_DIR, SHOPIFY_THEME_FILE_NAME))

if __name__ == "__main__":
    backup()
