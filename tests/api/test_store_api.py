import pytest
from pydantic import BaseModel
from api_clients.store_api import StoreAPI


class ProductSchema(BaseModel):
    id: int
    title: str
    price: float
    category: str


@pytest.fixture(scope="module")
def api():
    return StoreAPI()


def test_login_success(api):
    response = api.login("emilys", "emilyspass")
    assert response.status_code == 200
    data = response.json()
    assert "accessToken" in data
    assert data["username"] == "emilys"


def test_login_invalid_credentials(api):
    response = api.login("emilys", "wrong_password_123")
    assert response.status_code == 400
    assert "Invalid credentials" in response.json().get("message", "")


def test_get_products_pagination_and_schema(api):
    response = api.get_products(limit=5, skip=0)
    assert response.status_code == 200
    data = response.json()
    assert len(data["products"]) == 5
    for item in data["products"]:
        ProductSchema(**item)


def test_search_products(api):
    query = "phone"
    response = api.search_products(query)
    assert response.status_code == 200
    products = response.json()["products"]
    assert len(products) > 0
    for product in products:
        text = f"{product['title']} {product['description']}".lower()
        assert query in text


def test_get_non_existent_product(api):
    response = api.get_product_by_id(999999)
    assert response.status_code == 404


def test_add_cart_calculation(api):
    products_to_add = [{"id": 1, "quantity": 2}, {"id": 2, "quantity": 1}]
    response = api.add_cart(user_id=1, products=products_to_add)
    assert response.status_code == 201
    data = response.json()
    assert data["totalQuantity"] == 3
    assert data["total"] > 0
    assert data["discountedTotal"] <= data["total"]
