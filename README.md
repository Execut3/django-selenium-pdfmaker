# django-selenium-pdfmaker
A Light Django Application which uses selenium to convert any html page to pdf. Using this approach you can easily make pdf of HTML pages with charts, tables and having their loaded Styles.


## Install

Install easily via pip:

```
pip install django-selenium-pdfmaker
```

Then add package name `django_selenium_pdfmaker` to the INSTALLED_APPS of django.

### Installation of Google-Chrome & chromedriver

To use this package, `google-chrome` and proper `chromedriver` should be installed on your Operating System.

To install google chrome:

```bash
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add 
sudo bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list" 
sudo apt -y update 
sudo apt -y install google-chrome-stable 
```

And to have latest `chromedriver` A python management command is developed:

```bash
./manage.py pdfmaker_install_chromedriver
```

## Usage

To use this module, try to create an instance of `PDFMaker` class, then call `get_pdf_from_html` method.

```python
from django_selenium_pdfmaker.modules import PDFMaker
pdfmaker = PDFMaker()
res = pdfmaker.get_pdf_from_html(url='https://google.com', filename='output', write=True)
```

Which will load url in chromedriver and return proper results in `res` json. which includes:

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

## Settings

```
CHROMEDRIVER_PATH
```
Override this variable to address the binary file of chromedriver of your own. Optional.

```
SELENIUM_DELAY
```
To set delay on selenium requests (default 3). it will last that amount of time crawling
requested page before closing the session and create pdf of it. Optional and default to 0.

## Exceptions

##### 1- Message: session not created: This version of ChromeDriver only supports Chrome version 90 Current browser version is 103.0.5060.53 with binary path /usr/bin/google-chrome
If you faced a problem like this, you should address the correct chromedriver binary in your codes.
To do that download the proper chromedriver version and place in your OS. Then address it with following option in
your `settings.py` file:

```bash
CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
```

Also you can use below script to automatically fix this problem:

```bash
pip install webdriver-manager
```

Then use the driver in python as follows

```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
```
You can find the solution [link](https://stackoverflow.com/questions/60296873/sessionnotcreatedexception-message-session-not-created-this-version-of-chrome)
