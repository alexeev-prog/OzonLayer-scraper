import json
import logging
import ssl
from pathlib import Path

from utils.collect_product_data import collect_data
from utils.load_in_excel import write_data_to_excel
from utils.prepare_work import preparation_before_work
from utils.scroll import page_down
from utils.write_products_urls_in_file import write_products_urls

ssl._create_default_https_context = ssl._create_unverified_context
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

PATH_DATA_PRODUCTS_NAME = "PRODUCTS_DATA.json"


def main() -> None:
    try:
        logging.info("[INFO] Сбор данных начался. Пожалуйста, ожидайте...")
        driver = preparation_before_work()

        products_urls_list = page_down(driver=driver)
        write_products_urls(products_urls=products_urls_list)

        path_urls_products = Path("products_urls_dict_small.json")
        with path_urls_products.open("r", encoding="utf-8") as file:
            products_urls = json.load(file)

        collect_data(products_urls=products_urls, driver=driver)

        driver.quit()

        path_data_products = Path(PATH_DATA_PRODUCTS_NAME)
        with path_data_products.open("r", encoding="utf-8") as file:
            products_data = json.load(file)

        write_data_to_excel(products_data=products_data)

    except Exception as e:
        logging.exception(f"При выполнении программы произошла ошибка: {e}")
    else:
        logging.info("Работа выполнена успешно!")


if __name__ == "__main__":
    main()
