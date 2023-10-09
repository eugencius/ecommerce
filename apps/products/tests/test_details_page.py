from django.urls import reverse

from .product_test_base import ProductBaseTest


class TestDetailsPage(ProductBaseTest):
    def setUp(self):
        super().setUp()

        self.c001 = self.create_category(name="Category 001")
        self.c002 = self.create_category(name="Category 002")

        self.p001 = self.create_product(name="Product 001", category=self.c001)
        self.p002 = self.create_product(name="Product 002", category=self.c001)
        self.p003 = self.create_product(name="Product 003", category=self.c002)

    def get_details_page(self):
        url = reverse("products:details", kwargs={"slug": self.p001.slug})
        return self.client.get(url)

    def test_details_page_returns_code_200_OK(self):
        response = self.get_details_page()
        self.assertEqual(response.status_code, 200)

    def test_details_page_renders_correct_template(self):
        response = self.get_details_page()
        self.assertTemplateUsed(response, "products/details.html")

    def test_details_page_returns_code_404_when_is_published_is_false(self):
        self.p001.is_published = False
        self.p001.save()

        response = self.get_details_page()

        self.assertEqual(response.status_code, 404)

    def test_details_page_renders_just_products_from_the_same_category(self):
        response = self.get_details_page()

        related_products = response.context["related_products"]

        self.assertIn(self.p002, related_products)
        self.assertNotIn(self.p003, related_products)
