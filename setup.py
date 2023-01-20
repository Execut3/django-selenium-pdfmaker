from os import path
from setuptools import setup

project_path = path.abspath(path.dirname(__file__))

with open(path.join(project_path, 'README.md')) as f:
    long_description = f.read()

setup(
    name='django-selenium-pdfmaker',
    packages=['django_selenium_pdfmaker'],
    license='GPT',
    version='0.0.5',
    description='A Light Django Application which uses selenium to convert any html page to pdf. Using this approach you can easily make pdf of HTML pages with charts, tables and having their loaded Styles.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Reza Torkaman Ahmadi',
    author_email='execut3.binarycodes@gmail.com',
    url='https://github.com/Execut3/django-selenium-pdfmaker',
    keywords=['django', 'selenium', 'pdf', 'export-pdf', 'convert-html-to-pdf'],
    classifiers=[
        "Framework :: Django"
    ],
    install_requires=[
        "Django>=2.0",
        "selenium",
        "webdriver-manager",
    ],
    include_package_data=True,
)

# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository pypi dist/*
