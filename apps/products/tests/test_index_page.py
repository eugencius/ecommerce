from django.test import TestCase

from .product_test_base import ProductBaseTest


class ProductIndexTesting(ProductBaseTest):
    def test_index_returns_status_code_200_OK(self):
        response = self.get_index_response()

        self.assertEqual(response.status_code, 200)

    def test_index_renders_correct_template(self):
        response = self.get_index_response()
        self.assertTemplateUsed(response, "products/index.html")

    def test_index_renders_just_published_products(self):
        p001 = self.create_product(name="Product 001", is_published=True)
        p002 = self.create_product(name="Product 002", is_published=False)

        response = self.get_index_response()
        products_on_index = len(response.context["products"])

        self.assertEqual(products_on_index, 1)
