import pytest

from utils.apiBase import APIUtils


# pytest -m api


@pytest.mark.api
@pytest.mark.smoke
def test_get_products_list(playwright):
    api_utils = APIUtils()
    response = api_utils.getProductsList(playwright)
    assert response["responseCode"] == 200
    assert len(response["products"]) > 0


@pytest.mark.api
def test_post_to_products_list_not_supported(playwright):
    api_utils = APIUtils()
    response = api_utils.postToProductsList(playwright)
    assert response["responseCode"] == 405


@pytest.mark.api
def test_search_product(playwright):
    api_utils = APIUtils()
    response = api_utils.searchProduct(playwright, "top")
    assert response["responseCode"] == 200
    assert len(response["products"]) > 0
