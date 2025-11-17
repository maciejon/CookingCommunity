from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    # category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Ingredient {self.name}"

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category, related_name="recipes")

    description = models.TextField(blank=True)
    preparation_time = models.PositiveIntegerField()
    number_of_views = models.PositiveIntegerField(default=0)

    image = models.TextField(max_length=255, blank=True, null=True)

    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class RecipeStep(models.Model):
    step_number = models.PositiveIntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
    text = models.TextField()

    class Meta:
        ordering = ['step_number']
        unique_together = ('recipe', 'step_number')

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    # ingredient = models.CharField(max_length=255)
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
