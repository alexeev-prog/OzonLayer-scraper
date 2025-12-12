import logging
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from utils.config import CONFIG


def page_down(
    driver: WebDriver,
    pause_time: int | None = None,
    max_attempts: int | None = None,
    page_processed_max: int | None = None,
) -> list[str]:
    scroll_config = CONFIG["scroll"]
    class_name = scroll_config["class_name"]
    pause_time = pause_time or scroll_config["pause_time"]
    max_attempts = max_attempts or scroll_config["max_attempts"]
    page_processed_max = page_processed_max or scroll_config["page_processed_max"]

    logging.info("[INFO] Начинаем прокрутку и сбор ссылок...")

    collected_links = set()
    last_height = driver.execute_script("return document.body.scrollHeight")
    attempts = 0
    pages_processed = 0

    while attempts < max_attempts and pages_processed < page_processed_max:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_links = set()

        try:
            find_links = driver.find_elements(By.CLASS_NAME, class_name)
            new_links = {
                link.get_attribute("href")
                for link in find_links
                if link.get_attribute("href")
            }
            collected_links.update(new_links)
        except Exception as e:
            logging.exception(f"[!] Ошибка при сборе ссылок: {e}")

        pages_processed += 1

        logging.info(
            f"[PAGE {pages_processed}] Новые ссылки: {len(new_links)}; Всего ссылок обработано: {len(collected_links)}"
        )

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            attempts += 1
        else:
            attempts = 0

        last_height = new_height

    logging.info(f"[INFO] Сбор завершен, найдено {len(collected_links)} ссылок.")
    return list(collected_links)
