from django.core.management.base import BaseCommand

from webdriver_manager.chrome import ChromeDriverManager


class Command(BaseCommand):

    def handle(self, *args, **options):
        # To use this package, chromedriver should be installed on OS system.
        # To have this newest chromedriver we will use code below to install the latest version of it.
        try:
            driver_path = ChromeDriverManager().install()
            print(f'Installed Driver at path {driver_path}')
        except Exception as e:
            print('[-] Error Installing ChromeDriver', e)
