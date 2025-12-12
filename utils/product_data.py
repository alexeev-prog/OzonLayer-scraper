# utils/product_data.py
import logging
import time as tm

from bs4 import BeautifulSoup, Tag
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from utils.config import CONFIG


def _get_stars_reviews(soup: BeautifulSoup) -> tuple[str | None, str | None]:
    try:
        product_statistic = soup.find(
            "div",
            attrs={"data-widget": CONFIG["product"]["rating_widget"]},
        )
        if product_statistic and " • " in product_statistic.text:
            product_stars = product_statistic.text.split(" • ")[0].strip()
            product_reviews = product_statistic.text.split(" • ")[1].strip()
            return product_stars, product_reviews
        return None, None
    except Exception as e:
        logging.exception(f"Ошибка при получении рейтинга и отзывов: {e}")
        return None, None


def _get_sale_price(soup: BeautifulSoup) -> str | None:
    try:
        price_element = soup.find(
            "span", string=CONFIG["product"]["price_element_text"]
        )
        if not price_element or not price_element.parent:
            return None

        price_container = price_element.parent.find("div")
        if not price_container:
            return None

        price_span = price_container.find("span")
        if not price_span or not price_span.text:
            return None

        return price_span.text.strip().replace("\u2009", "")
    except Exception as e:
        logging.exception(f"Ошибка при получении цены с Ozon Картой: {e}")
        return None


def _get_full_prices(soup: BeautifulSoup) -> tuple[str | None, str | None]:
    try:
        price_element = soup.find("span", string=CONFIG["product"]["base_price_text"])
        if (
            not price_element
            or not price_element.parent
            or not price_element.parent.parent
        ):
            return None, None

        price_containers = price_element.parent.parent.find("div")
        if not price_containers:
            return None, None

        price_spans = price_containers.find_all("span")

        def _clean_price(price: str) -> str:
            return price.replace("\u2009", "").replace("₽", "").strip() if price else ""

        product_discount_price = (
            _clean_price(price_spans[0].text.strip()) if price_spans else None
        )
        product_base_price = (
            _clean_price(price_spans[1].text.strip()) if len(price_spans) > 1 else None
        )

        return product_discount_price, product_base_price
    except Exception as e:
        logging.exception(f"Ошибка при получении полной цена: {e}")
        return None, None


def _get_product_name(soup: BeautifulSoup) -> str:
    try:
        heading_div = soup.find(
            "div", attrs={"data-widget": CONFIG["product"]["heading_widget"]}
        )
        if not isinstance(heading_div, Tag):
            return ""

        title_element = heading_div.find("h1")
        if not isinstance(title_element, Tag):
            return ""

        return title_element.text.strip().replace("\t", "").replace("\n", " ")
    except Exception as e:
        logging.exception(f"Ошибка при получении имени продукта: {e}")
        return ""


def _get_salesman_name(soup: BeautifulSoup) -> str | None:
    try:
        elements = soup.find_all("a", class_=CONFIG["product"]["salesman_class"])
        return elements[0].text if elements else None
    except Exception as e:
        logging.exception(f"Ошибка при получении имени продавца: {e}")
        return None


def _get_product_id(driver: WebDriver) -> str:
    try:
        element = driver.find_element(By.XPATH, CONFIG["product"]["product_id_xpath"])
        text = element.text
        if "Артикул: " in text:
            return text.split("Артикул: ")[1]
        return "Не указан"
    except Exception as e:
        logging.exception(f"Ошибка при получении ID продукта: {e}")
        return "Не указан"


def get_characteristics(soup: BeautifulSoup) -> dict[str, str]:
    characteristics = {}
    try:
        char_blocks = soup.find_all(
            "dl", class_=CONFIG["product"]["characteristics_class"]
        )
        for block in char_blocks:
            if not isinstance(block, Tag):
                continue
            dt = block.find("dt")
            dd = block.find("dd")
            if dt and dd:
                key = dt.get_text(strip=True)
                value = dd.get_text(strip=True)
                characteristics[key] = value
    except Exception as e:
        logging.exception(f"Ошибка при получении характеристик: {e}")
    return characteristics


def _get_colors(soup: BeautifulSoup) -> list[str]:
    colors = []
    try:
        color_container = soup.find(
            "div", class_=CONFIG["product"]["colors_container_class"]
        )
        if not color_container:
            return colors

        color_elements = color_container.find_all(
            "div", class_=CONFIG["product"]["color_item_class"]
        )
        for element in color_elements:
            color_div = element.find(
                "div", class_=CONFIG["product"]["color_name_class"]
            )
            color_value = None
            if color_div and color_div.has_attr("title"):
                color_value = color_div["title"]
            elif color_div:
                color_value = color_div.get_text(strip=True)

            if color_value and color_value.strip():
                colors.append(color_value.strip())
    except Exception as e:
        logging.exception(f"Ошибка при получении цветов: {e}")
    return colors


def collect_product_info(
    driver: WebDriver, url: str
) -> dict[str, str | None | dict | list]:
    try:
        start = tm.time()
        driver.switch_to.new_window("tab")
        tm.sleep(1)
        driver.get(url=url)
        tm.sleep(1)

        page_source = str(driver.page_source)
        soup = BeautifulSoup(page_source, "lxml")

        characteristics = get_characteristics(soup)
        colors = _get_colors(soup)

        product_data = {
            "product_id": _get_product_id(driver),
            "product_name": _get_product_name(soup),
            "product_ozon_card_price": _get_sale_price(soup),
            "product_discount_price": _get_full_prices(soup)[0],
            "product_base_price": _get_full_prices(soup)[1],
            "product_characteristics": characteristics,
            "product_colors": colors,
            "product_stars": _get_stars_reviews(soup)[0],
            "product_reviews": _get_stars_reviews(soup)[1],
            "salesman": _get_salesman_name(soup),
            "product_url": url,
        }

        end = tm.time()
        final = round(end - start, 3)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        logging.info(f"Собрана информация об {url} ({final}ms)")

        return product_data
    except Exception as e:
        logging.exception(f"Ошибка при сборе информации о продукте {url}: {e}")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return {}
