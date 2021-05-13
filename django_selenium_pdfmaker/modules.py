import os
import json
import time
import base64

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

MODULE_PATH = os.path.abspath(__file__)     # Get path of current module file (modules.py file)
DIR_PATH = os.path.dirname(MODULE_PATH)     # Folder of current python package for relative addressing.


class PDFMaker:
    driver = None
    delay = 3   # 3 second delay before creating snapshot of viewed page, to fully load html
    print_options = {}
    chromedriver = None

    def __init__(self, chromedriver=None, print_options=None, **kwargs):
        # This module uses google-chrome as driver of selenium to fetch pages!
        self.chromedriver = chromedriver if chromedriver else os.path.join(DIR_PATH, 'chromedriver')

        self.delay = kwargs.get('delay', 3)

        if print_options:
            self.print_options = print_options

        webdriver_options = Options()
        webdriver_options.add_argument('--headless')
        webdriver_options.add_argument('--disable-gpu')
        if kwargs.get('debug', False):
            webdriver_options.add_argument("--remote-debugging-port=9222")
        self.driver = webdriver.Chrome(self.chromedriver, options=webdriver_options)
        self.driver.set_window_size(1100, 1200)

    def send_devtools(self, cmd, params=None):
        if params is None:
            params = {}
        resource = f"/session/{self.driver.session_id}/chromium/send_command_and_get_result"
        url = self.driver.command_executor._url + resource
        body = json.dumps({'cmd': cmd, 'params': params})
        response = self.driver.command_executor._request('POST', url, body)
        if response.get('status'):
            raise Exception(response.get('value'))
        return response.get('value')

    def get_pdf_from_html(self, path):
        """ This method is used to """

        self.driver.get(path)

        # Add a delay so the page fully loaded,
        # Increase this value in case you have heavy loaded html page, which will be loaded longer!
        time.sleep(3)

        calculated_print_options = {
            'landscape': False,
            'displayHeaderFooter': False,
            'printBackground': True,
            'preferCSSPageSize': True,
        }
        calculated_print_options.update(self.print_options)
        result = self.send_devtools("Page.printToPDF", calculated_print_options)
        self.driver.quit()
        return base64.b64decode(result['data'])
