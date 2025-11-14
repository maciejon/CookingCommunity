from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class IngredientCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Ingredient Categories"

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(IngredientCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Ingredient {self.name} from {self.category} category"

class RecipieCategory(models.Model):
    name = models.CharField(max_length=255) 

    class Meta:
        verbose_name_plural = "Recipe Categories"   

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(RecipieCategory, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    time = models.PositiveIntegerField()

class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    text = models.TextField()

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    # rozne jednostki kuchenne
    class Unit(models.TextChoices):
        SPOON = 'łyżka'
        TEASPOON = 'łyżeczka'
        GLASS = 'szklanka'
        PIECE = 'sztuka'
        PINCH = 'szczypta'
        ML = 'ml'
        L = 'l'
        G = 'g'
        KG = 'kg'
        BLANK = ''

    # np 1,5 szklanki
    quantity = models.DecimalField(max_digits=7, decimal_places=2)
    unit_choice = models.CharField(max_length=20, choices=Unit.choices, blank=True, default=Unit.BLANK) 

    UNIT_FORMS = {
        Unit.SPOON: ('łyżka', 'łyżki', 'łyżek'),
        Unit.TEASPOON: ('łyżeczka', 'łyżeczki', 'łyżeczek'),
        Unit.GLASS: ('szklanka', 'szklanki', 'szklanek'),
        Unit.PIECE: ('sztuka', 'sztuki', 'sztuk'),
        Unit.PINCH: ('szczypta', 'szczypty', 'szczypt'),
        Unit.ML: ('ml', 'ml', 'ml'),
        Unit.L: ('l', 'l', 'l'),
        Unit.G: ('g', 'g', 'g'),
        Unit.KG: ('kg', 'kg', 'kg'),
    }

    simple_units = [Unit.ML, Unit.L, Unit.G, Unit.KG]

    @property
    def unit(self):
        if not self.unit_choice or self.quantity is None or self.unit_choice == self.Unit.BLANK:
            return ""
        
        if self.unit_choice in self.simple_units:
            return self.unit_choice

        forms = self.UNIT_FORMS.get(self.unit_choice)

        # przemyslec czy tam moze None kiedys wejsc
        if isinstance(self.quantity, Decimal) and self.quantity % 1 != 0:
            return forms[1]

        q_int = int(self.quantity)
        
        # liczba poj
        if q_int == 1:
            return forms[0] 

        # ostatni znak 2,3,4 -> koncowka -i; z wyjatkiem nascie
        last_digit = q_int % 10
        if last_digit in [2, 3, 4] and q_int % 100 not in [12, 13, 14]:
            return forms[1] 
        
        # inne liczby to mnoga -ek
        return forms[2]
