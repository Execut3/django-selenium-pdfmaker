# django-selenium-pdfmaker
A Light Django Application which uses selenium to convert any html page to pdf. Using this approach you can easily make pdf of HTML pages with charts, tables and having their loaded Styles.


## Install

simply just using pip:

```
pip install django_selenium_pdfmaker
```

## Usage

To use this module:

```python
from django_selenium_pdfmaker.modules import PDFMaker
pdfmaker = PDFMaker()
res = pdfmaker.get_pdf_from_html(path='https://google.com', filename='output', write=True)
```

and `res` includes:

```json
{
  "raw": "pdf in binary format",
  "pdf": "ConvertedPDF instance if write flag is True."
}
```