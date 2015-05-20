# coding: utf-8
__author__ = 'nico'

import json
import time

import jinja2
import webapp2

from facade import RecipeFacade, CategoryFacade

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates"),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # do_inserts()
        template = JINJA_ENVIRONMENT.get_template("index.html")
        self.response.write(template.render())


class AllRecipesHandler(webapp2.RequestHandler):
    def get(self):
        cat_code = self.request.get("category-filter")
        if cat_code == "":
            recipes = RecipeFacade().get_all()
        else:
            recipes = RecipeFacade().get_by_category(cat_code)
        template = JINJA_ENVIRONMENT.get_template("allrecipes.html")
        self.response.write(template.render(recipes=recipes))


class NewRecipeHandler(webapp2.RequestHandler):
    def get(self):
        cat = CategoryFacade().get_all()
        if len(cat) == 0:
            template = JINJA_ENVIRONMENT.get_template("allrecipes.html")
            error = "There is no categories created. Please create one before."
            self.response.write(template.render(error=error))
        else:
            template = JINJA_ENVIRONMENT.get_template("newrecipe.html")
            self.response.write(template.render(categories=cat))

    def post(self):
        name = str(self.request.get("name"))
        cat_code = str(self.request.get("category"))
        image = str(self.request.get("image"))
        servings = int(self.request.get("servings"))

        num_ingredients = int(self.request.get("numIngredients"))
        ing_list = ["ingredients" + num for num in map(str, range(num_ingredients))]
        ingredients = [self.request.get(i) for i in ing_list]

        quantities_list = ["quantities" + num for num in map(str, range(num_ingredients))]
        quantities = [self.request.get(q) for q in quantities_list]
        ing_dict = {ingredients[i]: quantities[i] for i in range(num_ingredients)}

        num_steps = int(self.request.get("numSteps"))
        steps_list = ["steps" + num for num in map(str, range(num_steps))]
        steps = [self.request.get(s) for s in steps_list]
        code = RecipeFacade().add(name, cat_code, image, servings, ing_dict, steps)
        r = RecipeFacade().get(code)
        template = JINJA_ENVIRONMENT.get_template("recipedetail.html")
        self.response.write(template.render(recipe=r))


class EditRecipeHandler(webapp2.RequestHandler):
    def get(self):
        code = self.request.get('recipe_id')
        cat = CategoryFacade().get_all()
        template = JINJA_ENVIRONMENT.get_template("editrecipe.html")
        r = RecipeFacade().get(code)
        self.response.write(template.render(categories=cat, recipe=r))

    def post(self):
        code = self.request.get("recipe_id")
        name = self.request.get("name").encode('utf-8')
        cat_code = self.request.get("category")
        image = str(self.request.get("image"))
        servings = int(self.request.get("servings"))
        num_ingredients = int(self.request.get("numIngredients"))
        ing_list = ["ingredients" + num for num in map(str, range(num_ingredients))]
        ingredients = [self.request.get(i) for i in ing_list]
        quantities_list = ["quantities" + num for num in map(str, range(num_ingredients))]
        quantities = [self.request.get(q) for q in quantities_list]
        ing_dict = {ingredients[i]: quantities[i] for i in range(num_ingredients)}
        num_steps = int(self.request.get("numSteps"))
        steps_list = ["steps" + num for num in map(str, range(num_steps))]
        steps = [self.request.get(s) for s in steps_list]
        RecipeFacade().update(code, name, cat_code, image, servings, ing_dict, steps)
        r = RecipeFacade().get(code)
        template = JINJA_ENVIRONMENT.get_template("recipedetail.html")
        self.response.write(template.render(recipe=r))


class DeleteHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.get('recipe_id') != "":
            code = self.request.get('recipe_id')
            RecipeFacade().delete(code)
            time.sleep(0.2)
            self.redirect("/allrecipes")
        elif self.request.get('category_id') != "":
            code = self.request.get('category_id')
            CategoryFacade().delete(code)
            time.sleep(0.2)
            self.redirect("/categories")


class NewCategoryHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template("newcategory.html")
        self.response.write(template.render())

    def post(self):
        name = str(self.request.get("name"))
        description = str(self.request.get("description"))
        image = str(self.request.get("image"))
        _ = CategoryFacade().add(name, description, image)
        time.sleep(0.2)
        categories = CategoryFacade().get_all()
        template = JINJA_ENVIRONMENT.get_template("allcategories.html")
        self.response.write(template.render(categories=categories))


class EditCategoryHandler(webapp2.RequestHandler):
    def get(self):
        code = self.request.get('category_id')
        cat = CategoryFacade().get(code)
        template = JINJA_ENVIRONMENT.get_template("editcategory.html")
        print cat
        self.response.write(template.render(category=cat))

    def post(self):
        code = self.request.get("category_id")
        name = self.request.get("name").encode('utf-8')
        description = self.request.get("description").encode('utf-8')
        image = str(self.request.get("image"))
        CategoryFacade().update(code, name, description, image)
        time.sleep(0.2)
        categories = CategoryFacade().get_all()
        template = JINJA_ENVIRONMENT.get_template("allcategories.html")
        self.response.write(template.render(categories=categories))


class RecipeDetailHandler(webapp2.RequestHandler):
    def get(self):
        code = self.request.get('id')
        r = RecipeFacade().get(code)
        template = JINJA_ENVIRONMENT.get_template("recipedetail.html")

        self.response.write(template.render(recipe=r))


class ImageHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.get('recipe_id') != "":
            code = self.request.get('recipe_id')
            r = RecipeFacade().get(code)
            if r.image:
                self.response.headers['Content-Type'] = 'image/png'
                self.response.out.write(r.image)
            else:
                self.response.out.write('No image')
        elif self.request.get('category_id') != "":
            code = self.request.get('category_id')
            c = CategoryFacade().get(code)
            if c.image:
                self.response.headers['Content-Type'] = 'image/png'
                self.response.out.write(c.image)
            else:
                self.response.out.write('No image')


class AllCategoriesHandler(webapp2.RequestHandler):
    def get(self):
        categories = CategoryFacade().get_all()
        template = JINJA_ENVIRONMENT.get_template("allcategories.html")
        self.response.write(template.render(categories=categories))


class SearchHandler(webapp2.RequestHandler):
    def get(self):
        chain = self.request.get("chain")
        rec = RecipeFacade().search(chain)
        self.response.write(json.dumps({"query": chain, "suggestions": rec}))
