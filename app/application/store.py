from dataclasses import asdict, dataclass

@dataclass(frozen=True)
class Product:
    id: int
    name: str
    description: str
    price: float

PRODUCTS = [
    Product(1, "Desktop", "Developer Desktop", 899.99),
    Product(2, "Mechanical Keyboard", "USB mechanical keyboard", 89.99),
    Product(3, "Wireless Mouse", "Ergonomic wireless mouse", 39.99),
    Product(4, "USB-C Dock", "Multi-port USB-C docking station", 129.99),
]

def list_products() -> list[dict]:
    return [asdict(product) for product in PRODUCTS]

def find_product(product_id: int) -> dict | None:
    product = next((product for product in PRODUCTS if product.id == product_id), None)
    return asdict(product) if product else None
