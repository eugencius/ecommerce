from .product_test_base import ProductBaseTest


class ProductModelTest(ProductBaseTest):
    def setUp(self):
        super().setUp()

        self.product001 = self.create_product(name="Product 001")

    def test_str_method_of_product_returns_the_name(self):
        self.assertEqual(str(self.product001), "Product 001")
