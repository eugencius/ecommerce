from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .product_test_base import ProductBaseTest


class TestCartPage(ProductBaseTest):
    def setUp(self):
        super().setUp()
        self.p001 = self.create_product(name="Product 001")

    def get_cart_page(self):
        url = reverse("products:cart")
        return self.client.get(url)

    def test_cart_page_returns_code_200_OK(self):
        response = self.get_cart_page()
        self.assertEqual(response.status_code, 200)

    def test_cart_page_renders_correct_template(self):
        response = self.get_cart_page()
        self.assertTemplateUsed(response, "products/cart.html")

    def test_cart_returns_empty_message(self):
        response = self.get_cart_page()
        response_content = response.content.decode("utf-8")

        expected_message = str(_("Your shopping cart is currently empty"))
        self.assertIn(expected_message, response_content)

    def test_cart_renders_product(self):
        self.product_to_cart(self.p001.pk)

        response = self.get_cart_page()
        response_content = response.content.decode("utf-8")

        self.assertIn(self.p001.name, response_content)
