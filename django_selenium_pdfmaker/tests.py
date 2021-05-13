from django.test import TestCase

from .models import *
from .modules import *


class WhateverTest(TestCase):

    def test_html_to_pdf(self):
        """ A test case to call google.com and store it as pdf in media folder. """
        pdf_count = ConvertedPDF.objects.count()

        pdfmaker = PDFMaker()
        res = pdfmaker.get_pdf_from_html(path='https://google.com', filename='output', write=True)
        self.assertTrue(res.get('status'))
        self.assertTrue(res.get('raw', None))
        self.assertTrue(res.get('pdf', ''))

        pdf_obj = res.get('pdf')
        self.assertTrue(pdf_obj.url.startswith('/media/converted-pdf'))

        pdf_after_count = ConvertedPDF.objects.count()
        self.assertTrue(pdf_after_count == pdf_count + 1)

    def test_notworking_html_to_pdf(self):
        """ A test case to call a non-existing website. """
        pdf_count = ConvertedPDF.objects.count()

        pdfmaker = PDFMaker()
        res = pdfmaker.get_pdf_from_html(path='https://ggsgfgsdgsfdgsfdgfd.om', filename='output-wrong', write=True)
        self.assertFalse(res.get('status'))
        self.assertTrue(pdf_count == ConvertedPDF.objects.count())

