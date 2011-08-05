from jove.utils import find_home
from jove_catalog.service import FOLDER_NAME


def find_catalog(context, name=None):
    home = find_home(context)
    folder = home.get(FOLDER_NAME)
    if folder is not None:
        return folder.get(name)
