# To use this package, chromedriver should be installed on OS system.
# To have this newest chromebrowser we will use code below to install the latest version of it.
try:
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    driver = webdriver.Chrome(ChromeDriverManager().install())
    print('after install')
except Exception as e:
    print('[-] Error Installing ChromeDriver', e)
