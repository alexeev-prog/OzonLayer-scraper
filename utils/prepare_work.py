import logging
import time

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utils.config import CONFIG


def preparation_before_work(item_name: str | None = None) -> WebDriver:
    search_config = CONFIG["search"]
    item_name = item_name or search_config["item_name"]

    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    try:
        driver = uc.Chrome(
            options=options,
            driver_executable_path="/nix/store/8g7r5x2lssp6rmdghw7bss77gx6fhsda-undetected-chromedriver-138.0.7204.157/bin/undetected-chromedriver",
        )
        driver.implicitly_wait(5)

        driver.get(url=search_config["url"])
        time.sleep(2)

        find_input = driver.find_element(By.NAME, search_config["input_name"])
        find_input.clear()
        time.sleep(2)
        find_input.send_keys(item_name)
        time.sleep(2)
        find_input.send_keys(Keys.ENTER)
        time.sleep(2)

        return driver
    except Exception as e:
        logging.exception(f"Ошибка при подготовке драйвера: {e}")
        raise
