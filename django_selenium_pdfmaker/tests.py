from django.test import TestCase

from .modules import *


class WhateverTest(TestCase):

    def test_connection(self):
        print('here')
        self.assertTrue(True)

        pdfmaker = PDFMaker()
        result = pdfmaker.get_pdf_from_html(path='https://google.com')
        print(result)
