import pytest
from pageObjects.products import ProductsPage

@pytest.mark.smoke
@pytest.mark.ui
def test_search_product(page):
    productsPage = ProductsPage(page)
    productsPage.searchProduct("Men Tshirt")
    productsPage.verifySearchResults("Men Tshirt")