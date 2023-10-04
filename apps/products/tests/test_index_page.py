from django.test import TestCase
from django.urls import reverse

from apps.products.models import Product


class ProductIndexTesting(TestCase):
    def get_index_response(self):
        url = reverse("products:index")
        return self.client.get(url)

    def create_product(self, is_published=False):
        return Product.objects.create(
            name="Product 001",
            short_description="Lorem ipsum dolor sit amet.",
            long_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas lacinia fringilla pharetra. Duis sem arcu, eleifend quis scelerisque fermentum, venenatis a lectus.",
            price=1200,
            promotional_price=1099,
            cover="media/images/media/images/iphone.jpg",
            stock=12,
            is_published=is_published,
        )

    def test_index_returns_status_code_200_OK(self):
        response = self.get_index_response()

        self.assertEqual(response.status_code, 200)

    def test_index_renders_correct_template(self):
        response = self.get_index_response()
        self.assertTemplateUsed(response, "products/index.html")

    def test_index_renders_just_published_products(self):
        p001 = self.create_product(is_published=True)
        p002 = self.create_product(is_published=False)

        response = self.get_index_response()
        products_on_index = len(response.context["products"])

        self.assertEqual(products_on_index, 2)
