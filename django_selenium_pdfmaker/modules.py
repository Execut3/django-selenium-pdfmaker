import json
import base64
import json
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from django.utils.translation import ugettext_lazy as _
from .settings import *

MODULE_PATH = os.path.abspath(__file__)  # Get path of current module file (modules.py file)
DIR_PATH = os.path.dirname(MODULE_PATH)  # Folder of current python package for relative addressing.


class PDFMaker:
    """ Main class to handle methods to capture an html page into pdf.

    Structure is as follow:
    - initiate class objects with provided attributes.
    - use selenium to visit url-path and convert it to pdf
    - write pdf in database and media/converted-pdf folder.
    """

    driver = None
    print_options = {}
    chromedriver_path = None
    delay = settings.SELENIUM_DELAY  # second delay before creating snapshot of viewed page, to fully load html

    save_file = True
    pdf_path = ''
    url_path = ''  # Will be overrided

    def __init__(self, **kwargs):
        # This module uses google-chrome as driver of selenium to fetch pages!
        if settings.CHROMEDRIVER_PATH:
            self.chromedriver_path = settings.CHROMEDRIVER_PATH
        else:
            self.chromedriver_path = ChromeDriverManager().install()

        # A simple delay to make driver waits to page fully loaded,
        # Increase if your page is heavy and late.
        if 'delay' in kwargs.keys():
            self.delay = kwargs.get('delay')

        options = Options()
        options.add_argument("headless")                    # open Browser in maximized mode
        options.add_argument("disable-infobars")            # disabling infobars
        options.add_argument("--disable-extensions")        # disabling extensions
        options.add_argument("--disable-gpu")               # applicable to windows os only
        options.add_argument("--disable-dev-shm-usage")     # overcome limited resource problems
        options.add_argument("--no-sandbox")                # Bypass OS security model
        # caps = DesiredCapabilities().CHROME
        # caps["pageLoadStrategy"] = "none"                   # Do not wait for full page
        self.driver = webdriver.Chrome(
            options=options,
            executable_path=self.chromedriver_path
        )
        # # self.driver.set_window_size(1100, 1200)

    def send_devtools(self, cmd, params=None):
        """ Check page, get content and convert to pdf. """
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

    def get_pdf_from_html(self, url=None, filename='output-pdf', write=True, **kwargs):
        """
        main method to call to make pdf.

        @:param filename: default output file name will be output-pdf.pdf
        @:param write: if True, meaning write to database on model ConvertedPDF
        """
        response = {
            'status': False,    # Status of operation
            'pdf': None,        # pdf object (ConvertedPDF instance)
            'raw': None,        # Raw data binary of output pdf
            'message': ''
        }

        # For backward compatibility
        if not url:
            url = kwargs.get('path', None)

        self.url_path = url

        try:
            self.driver.get(self.url_path)
        except Exception as e:
            print(f'[-] Error happened fetching html page. {e}')
            response.update({
                'message': _('Unable to connect to request URL')
            })
            return response

        # Add a delay so the page fully loaded,
        # Increase this value in case you have heavy loaded html page, which will be loaded longer!
        if self.delay:
            time.sleep(self.delay)

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

        # Write into database within /media/converted-pdf folder!
        if write:
            pdf_obj = self.store_to_file(result, filename)
            response.update({'pdf': pdf_obj})

        response.update({
            'raw': result,
            'status': True,
        })
        return response
