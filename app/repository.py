import math

from app.models import Product

PRODUCTS = [
    Product(id=1, name="Zenbook 14 OLED", category="Laptop", price=42900),
    Product(id=2, name="ROG Zephyrus G14", category="Gaming Laptop", price=62900),
    Product(id=3, name="ProArt P16", category="Creator Laptop", price=79900),
    Product(id=4, name="TUF Gaming A15", category="Gaming Laptop", price=38900),
    Product(id=5, name="ROG Ally X", category="Handheld", price=26900),
    Product(id=6, name="ProArt Display PA279CRV", category="Monitor", price=15900),
]


def list_products(
    q: str | None = None,
    sort: str | None = None,
    order: str = "asc",
    page: int = 1,
    page_size: int = 20,
) -> dict:
    results = PRODUCTS.copy()

    if q:
        q_lower = q.lower()
        results = [
            p for p in results
            if q_lower in p.name.lower() or q_lower in p.category.lower()
        ]

    if sort == "name":
        results = sorted(results, key=lambda p: p.name, reverse=(order == "desc"))
    elif sort == "price":
        results = sorted(results, key=lambda p: p.price, reverse=(order == "desc"))

    total = len(results)
    total_pages = math.ceil(total / page_size) if page_size else 0
    start = (page - 1) * page_size
    items = results[start: start + page_size]

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


def get_product(product_id: int) -> Product | None:
    return next((product for product in PRODUCTS if product.id == product_id), None)

