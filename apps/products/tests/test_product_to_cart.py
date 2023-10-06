from .product_test_base import ProductBaseTest


class TestProductToCart(ProductBaseTest):
    def setUp(self):
        self.product001 = self.create_product(name="Product 001")

        super().setUp()

    def test_adding_product_to_cart(self):
        self.product_to_cart(self.product001.pk)
        cart = self.client.session["cart"]

        self.assertIn(str(self.product001.pk), cart)
        self.assertEqual(len(cart), 1)

    def test_add_a_product_more_than_once(self):
        pk = str(self.product001.pk)

        self.product_to_cart_x_times(pk, 2)
        quantity = self.client.session["cart"][pk]["quantity"]

        self.assertEqual(2, quantity)

    def test_quantity_price_is_correct(self):
        pk = str(self.product001.pk)
        self.product001.price = 1200
        self.product001.save()

        self.product_to_cart_x_times(pk, 2)

        quantity_price = self.client.session["cart"][pk]["quant_price"]
        self.assertEqual(quantity_price, 2400)

    def test_quantity_promotional_price_is_correct(self):
        pk = str(self.product001.pk)
        self.product001.promotional_price = 900
        self.product001.save()

        self.product_to_cart_x_times(pk, 2)

        quantity_price = self.client.session["cart"][pk]["quant_promotional_price"]
        self.assertEqual(quantity_price, 1800)
