from selenium import webdriver

def get_web_driver(headless=True):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    if headless:
        options.add_argument('--headless')
    return webdriver.Chrome(options)
