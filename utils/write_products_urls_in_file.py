import json
import logging
import time
from pathlib import Path


def write_products_urls(
    products_urls: list[str], filename: str = "products_urls_dict_small.json"
) -> None:
    try:
        products_urls_dict = {str(k): v for k, v in enumerate(products_urls)}
        path_products_url = Path(filename)

        with path_products_url.open("w", encoding="utf-8") as file:
            json.dump(products_urls_dict, file, indent=4, ensure_ascii=False)

        time.sleep(2)
        logging.info(f"URLы продуктов успешно записаны в файл {filename}")
    except Exception as e:
        logging.exception(f"Ошибка при записи URLов продуктов: {e}")
        raise
