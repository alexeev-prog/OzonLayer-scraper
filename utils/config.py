CONFIG = {
    "scroll": {
        "class_name": "tile-clickable-element",
        "pause_time": 2,
        "max_attempts": 3,
        "page_processed_max": 1,
    },
    "product": {
        "rating_widget": "webSingleProductScore",
        "price_element_text": "c Ozon Картой",
        "base_price_text": "без Ozon Карты",
        "heading_widget": "webProductHeading",
        "salesman_class": "pdp_ae5",
        "characteristics_class": "pdp_ha9",
        "product_id_xpath": '//div[contains(text(), "Артикул: ")]',
        "colors_container_class": "pdp_q6",
        "color_item_class": "ea5_3_5-a",
        "color_name_class": "pdp_e7",
    },
    "excel": {"filename": "products.xlsx", "sheet_name": "Products"},
    "search": {
        "item_name": "Косметика",
        "url": "https://ozon.ru",
        "input_name": "text",
    },
}
