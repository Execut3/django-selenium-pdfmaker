from django.test import TestCase

from .modules import *


class WhateverTest(TestCase):

    def test_connection(self):
        print('here')
        self.assertTrue(True)

        pdfmaker = PDFMaker()
        result = pdfmaker.get_pdf_from_html(path='https://google.com')
        print(result)


        # # Store in file and database model!
        # file_name = '{}, {}.pdf'.format(self.fullname, self.identifier)
        # folder_path = os.path.join(MEDIA_ROOT, 'washup')
        # if not os.path.exists(folder_path):
        #     os.makedirs(folder_path)
        # file_path = os.path.join(folder_path, file_name)
        # with open(file_path, 'wb') as file:
        #     file.write(result)
        #
        # self.pdf = 'washup/{}'.format(file_name)