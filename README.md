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
  "status": true,
  "raw": "pdf in binary format",
  "pdf": "ConvertedPDF instance if write flag is True.",
  "message": ""
}
```

- `status` is `true` when converting to pdf is successful, else will be `false`.
For example when url path is unreachable `status` will be `false`.
- `raw` is binary data of pdf before storing in file. Will hold data if `status == true`
- `pdf` is `ConvertedPDF` object if `status` is `true`.
- `message` will hold reason why `status` is `false`.

