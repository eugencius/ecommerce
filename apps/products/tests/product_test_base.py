from django.test import TestCase
from django.urls import reverse

from apps.products.models import Category, Product


class ProductBaseTest(TestCase):
    def setUp(self):
        self.category = self.create_category()

    def get_index_response(self):
        url = reverse("products:index")
        return self.client.get(url)

    def create_category(self, name="General"):
        return Category.objects.create(
            name=name,
        )

    def create_product(
        self,
        name="Product 001",
        category=None,
        short_description="Lorem ipsum dolor sit amet.",
        long_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas lacinia fringilla pharetra. Duis sem arcu, eleifend quis scelerisque fermentum, venenatis a lectus.",
        price=1200,
        promotional_price=1100,
        cover="/home/vinicius/Pictures/project-images/iphone14.jpeg",
        stock=5,
        is_published=True,
    ):
        return Product.objects.create(
            name=name,
            category=category if category else self.category,
            short_description=short_description,
            long_description=long_description,
            price=price,
            promotional_price=promotional_price,
            cover=cover,
            stock=stock,
            is_published=is_published,
        )

    def product_to_cart(self, product_pk):
        url = reverse("products:to-cart", kwargs={"pk": product_pk})
        return self.client.post(url)

    def product_to_cart_x_times(self, product_pk, times=2):
        for i in range(0, times):
            self.product_to_cart(product_pk)
