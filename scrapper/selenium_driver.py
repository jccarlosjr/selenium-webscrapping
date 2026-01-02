# scrapper/selenium_driver.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException

from .config import LOCAL_USER_PATH

_driver = None


def init_driver():
    global _driver

    if _driver:
        try:
            _driver.title
            return _driver
        except WebDriverException:
            _driver = None

    chrome_service = ChromeService(ChromeDriverManager().install())

    options = webdriver.ChromeOptions()
    options.add_argument(LOCAL_USER_PATH)

    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--remote-debugging-port=9222")


    _driver = webdriver.Chrome(
        service=chrome_service,
        options=options
    )
    _driver.maximize_window()

    return _driver


def close_driver():
    global _driver
    if _driver:
        _driver.quit()
        _driver = None
