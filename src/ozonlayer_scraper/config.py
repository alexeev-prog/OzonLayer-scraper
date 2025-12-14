from pydantic import BaseModel, Field


class WebdriverConfig(BaseModel):
    binarypath: str = Field(default=..., description="Path to webdriver binary file")


class ParsingScrollConfig(BaseModel):
    class_name: str = Field(default=..., description="HTML class name for scrolling")
    pause_time: int = Field(default=2, description="Pause time in seconds")
    max_attempts: int = Field(default=3, description="Max attempts to scroll")
    page_processed_max: int = False(default=1, description="Page Processed max")


class ProductScrollConfig(BaseModel):
    rating_widget: str = Field(
        default="webSingleProductScore", description="Rating widget of product"
    )
    price_element_text: str = Field(
        default="c Ozon Картой", description="Price element (with ozon card)"
    )
    base_price_text: str = Field(
        default="без Ozon Карты", description="Base price element (without ozon card)"
    )
    heading_widget: str = Field(
        default="webProductHeading", description="Heading widget"
    )
    salesman_class: str = Field(default=..., description="Salesman class")
    characteristics_class: str = Field(
        default=..., description="Class of product parameters"
    )
    product_id_xpath: str = Field(
        default='//div[contains(text(), "Артикул: ")]',
        description="Product in in XPath format",
    )
    colors_container_class: str = Field(
        default=..., description="Colors container class"
    )
    color_item_class: str = Field(default=..., description="Color item class")
    color_name_class: str = Field(default=..., description="Color name class")


class ExcelConfig(BaseModel):
    filename: str = Field(
        default="products.xlsx", description="Filename for excel table"
    )
    sheet_name: str = Field(
        default="Products", description="Sheet name for excel table"
    )


class SearchConfig(BaseModel):
    item_name: str = Field(default=..., description="Item name")
    url: str = Field(default="https://ozon.ru", description="URL to ozon")
    input_name: str = Field(default=..., description="Input field name")
