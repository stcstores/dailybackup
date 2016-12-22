import os

from tabler import Tabler as Table

from linnworks_db import LinkingTable
from linnworks_db import InventoryTable
from linnworks_db import EbayTable
from linnworks_db import PropertiesTable

from stclocal import IMPORT_DIR


def update_linking(
        update_file=os.path.join(IMPORT_DIR, 'linnworks_linking.csv')):
    """Updates linking table from update_file """
    LinkingTable().update_from_file(Table(update_file))


def update_inventory(
        update_file=os.path.join(IMPORT_DIR, 'linnworks_inventory.csv')):
    """Updates inventory table from update_file """
    InventoryTable().update_from_file(Table(update_file))


def update_ebay(
        update_file=os.path.join(IMPORT_DIR, 'ebay_products.csv')):
    """Updates ebay table from update_file """
    EbayTable().print_update(Table(update_file))


def update_properties(
        update_file=os.path.join(IMPORT_DIR, 'custom_properties.csv')):
    """Updates properties table from update_file """
    PropertiesTable().print_update(Table(update_file))


def update_all():
    update_linking()
    update_inventory()
    update_ebay()
    update_properties()
