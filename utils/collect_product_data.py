import json
import logging
import time
from pathlib import Path

from selenium.webdriver.chrome.webdriver import WebDriver

from utils.product_data import collect_product_info


def writing_product_data_in_file(
    products_data: dict[str, dict[str, str | None]],
    filename: str = "PRODUCTS_DATA.json",
) -> None:
    try:
        path = Path(filename)
        with path.open("w", encoding="utf-8") as file:
            json.dump(products_data, file, indent=4, ensure_ascii=False, sort_keys=True)
        logging.info(f"Данные успешно записаны в файл {filename}")
    except Exception as e:
        logging.exception(f"Ошибка при записи данных в файл: {e}")
        raise


def collect_data(
    products_urls: dict[str, str],
    driver: WebDriver,
) -> None:
    products_data = {}

    for url in products_urls.values():
        try:
            data = collect_product_info(driver=driver, url=url)
            product_id = data.get("product_id")
            if product_id and product_id not in products_data:
                products_data[product_id] = data
            time.sleep(1)
        except Exception as e:
            logging.exception(f"Ошибка при сборе данных для URL {url}: {e}")
            continue

    writing_product_data_in_file(products_data=products_data)
