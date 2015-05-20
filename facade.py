# coding: utf-8
__author__ = 'nico'

from entities import Recipe, Ingredient, Category
from daos import RecipeDAO, CategoryDAO
from utils import Singleton


class RecipeFacade:
    """
    Class that contains all business logic related to Recipes.
    """

    __metaclass__ = Singleton

    def __init__(self):
        self.dao = RecipeDAO()

    def add(self, name, cat_code, image, servings, ingredients_dict, steps):
        """
        Add a new Recipe.
        @param name: Name of the recipe.
        @param cat_code: Code of the category.
        @param image: Image of the recipe.
        @param servings: Number of servings.
        @param ingredients_dict: Dictionary that contains ingredient information.
        @param steps: List that contains all steps.
        @return: Code of the recipe.
        """
        category = CategoryFacade().get(cat_code)
        category.id = CategoryFacade().get_by_name(category.name).id
        ingredients = [Ingredient(name=i, quantity=q) for i, q in ingredients_dict.items()]
        r = Recipe(name=name, category=category, image=image, servings=servings, ingredients=ingredients,
                   steps=steps)
        return self.dao.save(r)

    def update(self, code, name, cat_code, image, servings, ingredients, steps):
        """
        Updates a recipe with giving code.
        @param code: Code of the recipe.
        @param name: Name of the recipe.
        @param cat_code: Code of the category.
        @param image: Image of the recipe.
        @param servings: Number of servings.
        @param ingredients: Dictionary that contains ingredient information.
        @param steps: List that contains all steps.
        """
        r = self.dao.get(code)
        r.name = name
        r.servings = servings
        if image != "":
            r.image = image
        r.category = CategoryFacade().get(cat_code)
        r.ingredients = [Ingredient(name=n, quantity=q) for n, q in ingredients.items()]
        r.steps = steps
        self.dao.update(r)

    def get(self, code):
        """
        Obtains a recipe by code.
        @param code: Code of the recipe.
        @return: Recipe object.
        """
        return self.dao.get(code)

    def delete(self, code):
        """
        Remove a recipe by code.
        @param code: Code of the recipe.
        """
        self.dao.delete(code)

    def get_all(self):
        """
        Obtains all recipes.
        @return: List with all recipes.
        """
        return self.dao.get_all()

    def get_by_category(self, cat_code):
        """
        Obtains all recipes from a giving category.
        @param cat_code: Code of category
        @return: List with all recipes from a giving category.
        """
        return self.dao.get_by_category(cat_code)

    def delete_by_category(self, cat_code):
        """
        Delete all recipes from a giving category.
        @param cat_code: Code of category
        """
        recipes = self.get_by_category(cat_code)
        for code in [r.key.urlsafe() for r in recipes]:
            self.dao.delete(code)

    def update_category_in_recipes(self, cat_code, category):
        """
        Updates category in recipes after recipe modification.
        @param cat_code: Code of the category.
        @param category: Category object.
        """
        recipes = self.get_by_category(cat_code)
        for r in recipes:
            r.category = category
            print r.category.name
            self.dao.update(r)

    def search(self, chain):
        """
        Obtains all recipes that match with a giving string.
        @param chain: Search text.
        @return: List with all recipes found.
        """
        return [{"value": r.name, "data": r.key.urlsafe()} for r in self.dao.search(chain)]


class CategoryFacade:
    """
    Class that contains all business logic related to Categories.
    """

    __metaclass__ = Singleton

    def __init__(self):
        self.dao = CategoryDAO()

    def add(self, name, description, image):
        """
        Adds a new category.
        @param name: Category name.
        @param description: Category description.
        @param image: Category image.
        """
        c = Category(name=name, description=description, image=image)
        self.dao.save(c)

    def update(self, code, name, description, image):
        """
        Updates a category with the giving data
        @param code: Category code.
        @param name: Category name.
        @param description: Category description.
        @param image: Category image.
        """
        c = self.dao.get(code)
        c.name = name
        c.description = description
        if image != "":
            c.image = image
        self.dao.update(c)
        RecipeFacade().update_category_in_recipes(code, c)

    def get(self, code):
        """
        Obtains a category by code.
        @param code: Category code.
        @return: Category object.
        """
        return self.dao.get(code)

    def get_by_name(self, name):
        """
        Obtains a category by name.
        @param name: Category name.
        @return: Category object.
        """
        return self.dao.get_by_name(name)

    def delete(self, code):
        """
        Removes category by code.
        @param code: Category code.
        """
        RecipeFacade().delete_by_category(code)
        self.dao.delete(code)

    def get_all(self):
        """
        Obtains all categories.
        @return: List with all categories.
        """
        return self.dao.get_all()

