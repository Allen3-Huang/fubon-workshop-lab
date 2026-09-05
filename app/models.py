import math

from pydantic import BaseModel, ConfigDict, Field, computed_field


class Product(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: int = Field(gt=0)
    name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    price: float = Field(gt=0)


class ProductPage(BaseModel):
    items: list[Product]
    total: int = Field(ge=0)
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def total_pages(self) -> int:
        if self.total == 0:
            return 0
        return math.ceil(self.total / self.page_size)

