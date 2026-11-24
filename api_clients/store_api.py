import requests


class StoreAPI:
    def __init__(self, base_url: str = "https://dummyjson.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def login(self, username: str, password: str) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/auth/login",
            json={"username": username, "password": password}
        )

    def get_products(self, limit: int = 10, skip: int = 0) -> requests.Response:
        return self.session.get(
            f"{self.base_url}/products",
            params={"limit": limit, "skip": skip}
        )

    def search_products(self, query: str) -> requests.Response:
        return self.session.get(
            f"{self.base_url}/products/search",
            params={"q": query}
        )

    def get_product_by_id(self, product_id: int) -> requests.Response:
        return self.session.get(f"{self.base_url}/products/{product_id}")

    def add_cart(self, user_id: int, products: list[dict]) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/carts/add",
            json={"userId": user_id, "products": products}
        )
