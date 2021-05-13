import os
import sys
import json
import time
import base64
import tempfile

from selenium import webdriver
from django.conf import settings
from django.core.files.base import ContentFile, File
from selenium.webdriver.chrome.options import Options
from django.utils.translation import ugettext_lazy as _
from django.core.files.uploadedfile import SimpleUploadedFile

MODULE_PATH = os.path.abspath(__file__)     # Get path of current module file (modules.py file)
DIR_PATH = os.path.dirname(MODULE_PATH)     # Folder of current python package for relative addressing.


class PDFMaker:
    """ Main class to handle methods to capture an html page into pdf.
    Structure is as follow:

    - initiate class objects with provided attributes.
    - use selenium to visit url-path and convert it to pdf
    - write pdf in database and media/converted-pdf folder.
    """

    driver = None
    delay = 3   # 3 second delay before creating snapshot of viewed page, to fully load html
    print_options = {}
    chromedriver = None

    save_file = True
    pdf_path = ''

    def __init__(self, chromedriver=None, print_options=None, **kwargs):
        # This module uses google-chrome as driver of selenium to fetch pages!
        self.chromedriver = chromedriver if chromedriver else os.path.join(DIR_PATH, 'chromedriver')

        # A simple delay to make driver waits to page fully loaded,
        # Increase if your page is heavy and late.
        self.delay = kwargs.get('delay', 3)

        # Creating options for webdriver (google-chrome)
        if print_options:
            self.print_options = print_options
        webdriver_options = Options()
        webdriver_options.add_argument('--headless')
        webdriver_options.add_argument('--disable-gpu')
        if kwargs.get('debug', False):
            webdriver_options.add_argument("--remote-debugging-port=9222")

        # Now create driver
        self.driver = webdriver.Chrome(self.chromedriver, options=webdriver_options)
        self.driver.set_window_size(1100, 1200)

    def send_devtools(self, cmd, params=None):
        """ Check page and convert to pdf. """
        if params is None:
            params = {}
        resource = f"/session/{self.driver.session_id}/chromium/send_command_and_get_result"
        url = self.driver.command_executor._url + resource
        body = json.dumps({'cmd': cmd, 'params': params})
        response = self.driver.command_executor._request('POST', url, body)
        if response.get('status'):
            raise Exception(response.get('value'))
        return response.get('value')

    def store_to_file(self, result, filename):
        """ Store pdf (result binary captured from prev step) into file and database.

        media path is: /media/converted-pdf/...
        """

        # Store in file and database model!
        from .models import ConvertedPDF

        c = ConvertedPDF(url='https://google.com')
        file_name = '{}.pdf'.format(filename)
        folder_path = os.path.join(settings.MEDIA_ROOT, 'converted-pdf')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'wb') as file:
            file.write(result)

        c.file = 'converted-pdf/{}'.format(file_name)
        c.save()

        return c.file

    def get_pdf_from_html(self, path, filename='output-pdf', write=True):
        """ main method to call to make pdf. """
        response = {
            'status': False,            # Status of operation
            'pdf': None,                # pdf object (ConvertedPDF instance)
            'raw': None,                # Raw data binary of output pdf
            'message': ''
        }

        try:
            self.driver.get(path)
        except Exception as e:
            print('[-] Error happened fetching html page.')
            response.update({
                'message': _('Unable to connect to request URL')
            })
            return response

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

        result = base64.b64decode(result['data'])


        if write:
            # Write into database within /media/converted-pdf folder!
            pdf_obj = self.store_to_file(result, filename)
            response.update({'pdf': pdf_obj})
        response.update({
            'raw': result,
            'status': True,
        })
        return response

