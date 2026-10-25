from django.db import models

class WasteInput(models.Model):
    CATEGORY_CHOICES = [
        ('food_waste', 'Mixed Food Waste'),
        ('swine_manure', 'Swine Manure'),
        ('cattle_manure', 'Cattle Manure'),
        ('wheat_straw', 'Wheat Straw'),
        ('corn_stover', 'Corn Stover'),
        ('spent_coffee', 'Spent Ground Coffee')
    ]
    latitude = models.FloatField(null=True, blank=True, help_text="Latitude of waste source")
    longitude = models.FloatField(null=True, blank=True, help_text="Longitude of waste source")
    
    # Baseline yield estimates (m³ of biogas per kg of fresh waste)
    # These can be refined later with precise lab parameters
    YIELD_FACTORS = {
        'food_waste': 0.150,
        'swine_manure': 0.030,
        'cattle_manure': 0.025,
        'wheat_straw': 0.300,
        'corn_stover': 0.250,
        'spent_coffee': 0.100,
    }

    waste_type = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    quantity_kg = models.FloatField(help_text="Input total waste in kilograms")
    date_logged = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantity_kg}kg of {self.get_waste_type_display()}"

    @property
    def estimated_biogas_yield(self):
        """Calculates the estimated biogas yield in cubic meters (m³)."""
        factor = self.YIELD_FACTORS.get(self.waste_type, 0)
        return round(self.quantity_kg * factor, 2)
        
    @property
    def estimated_electricity_kwh(self):
        """
        Converts biogas to electricity. 
        1 m³ of biogas generates approximately 2.1 kWh of electricity.
        """
        return round(self.estimated_biogas_yield * 2.1, 2)