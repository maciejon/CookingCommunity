from django.db import models

# class IngredientCategory(models.Model):
#     name = models.CharField(max_length=255)

# class Ingredient(models.Model):
#     name = models.CharField(max_length=255)
#     category = models.ForeignKey(IngredientCategory, on_delete=models.SET_NULL, null=True)

#     def __str__(self):
#         return f"Ingredient {self.name} from {self.category} category"

# class Recipe(models.Model):
#     name = models.CharField(max_length=255)

# class IngredientsForRecipe(models.Model):
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
#     ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)



