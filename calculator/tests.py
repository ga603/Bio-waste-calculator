from django.test import TestCase
from .forms import WasteInputForm
from .models import WasteInput


class WasteInputFormTests(TestCase):
    def test_coordinates_are_saved_including_zero_values(self):
        form = WasteInputForm(
            data={
                'waste_type': 'food_waste',
                'quantity_kg': '500',
                'latitude': '0',
                'longitude': '0',
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        waste_input = form.save()

        self.assertEqual(waste_input.latitude, 0)
        self.assertEqual(waste_input.longitude, 0)


class CalculatorViewTests(TestCase):
    def test_unsupported_language_falls_back_to_english(self):
        response = self.client.get('/?lang=unsupported')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SDG 7 &amp; 12: Bio-Waste Fermentation Calculator')
