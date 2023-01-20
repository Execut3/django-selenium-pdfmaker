import os
from django.conf import settings

MODULE_PATH = os.path.abspath(__file__)  # Get path of current module file (modules.py file)
DIR_PATH = os.path.dirname(MODULE_PATH)  # Folder of current python package for relative addressing.

# # Path to chromedriver should be provided, if not provided in project settings, use below!
# settings.CHROMEDRIVER_PATH = getattr(settings, 'CHROMEDRIVER_PATH', os.path.join(DIR_PATH, 'chromedriver'))
settings.CHROMEDRIVER_PATH = ''

# Delay to wait for page (html) to be loaded and generate pdf from it
settings.SELENIUM_DELAY = getattr(settings, 'SELENIUM_DELAY', 0)
