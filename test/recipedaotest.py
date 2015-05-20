# coding=utf-8
__author__ = 'nico'

import unittest

from google.appengine.ext import testbed

from entities import Recipe, Ingredient, Category
from daos import RecipeDAO


class RecipeDAOTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        self.rec_dao = RecipeDAO()

        self.rec1 = Recipe(name="Arroz con chícharos",
                           category=Category(name="Arroces"),
                           servings=4,
                           ingredients=[Ingredient(name="Arroz", quantity="500gr"),
                                        Ingredient(name="Chícharos", quantity="300gr")],
                           steps=["Cocemos o arroz", "Botámoslle os chícharos", "Servir en quente"])

        self.rec2 = Recipe(name="Macarróns con tomate",
                           category=Category(name="Pastas"),
                           servings=6,
                           ingredients=[Ingredient(name="Macarróns", quantity="600gr"),
                                        Ingredient(name="Tomate frito", quantity="100gr")],
                           steps=["Cocemos os macarróns",
                                  "Botámoslleo tomate frito",
                                  "Servimos en quente"])
        self.rec3 = Recipe(name="Gazpacho andaluz",
                           category=Category(name="Sopas e cremas"),
                           servings=6,
                           ingredients=[Ingredient(name="Aceite de oliva", quantity="120cc"),
                                        Ingredient(name="Auga", quantity="500cc"),
                                        Ingredient(name="Dente de allo", quantity="2"),
                                        Ingredient(name="Ovo duro", quantity="1"),
                                        Ingredient(name="Miga de pan", quantity="100gr"),
                                        Ingredient(name="Pepino", quantity="50gr"),
                                        Ingredient(name="Pemento verdeo", quantity="50gr"),
                                        Ingredient(name="Sal", quantity="1 pizca"),
                                        Ingredient(name="Tomates naturais", quantity="1kg"),
                                        Ingredient(name="Vinagre", quantity="60cc"),
                                        Ingredient(name="Cebola picada", quantity="1/2")],
                           steps=[
                               "No bol da batidora ponse o aceite, a vinagre, a sal e ben cortados, os allos, o pepino e o pemento."
                               " Triturase todo ben e vaise metendo na batidora",
                               "Vaise incorporando o tomate, previamente escaldado e pelado, e siguese pasando pola batidora",
                               "Ponse o pan en remollo e escorese e engadeselle o anterior",
                               "Incorporase a auga para que non quede tan espeso e uns cubiños de xeo para que este mais grio",
                               "Servese en tazons e en diferentes pratos individuais. Disponse un pouco de pemento picado, a "
                               "cebola, o pepino, o tomate natural e o ovo duro, previamente cocido, e todo elo finalmente "
                               "picado para engadir se se desexa ao gazpacho"])

        self.rec1key = self.rec1.put()
        self.assertEqual(Recipe.query().count(), 1, "Failed to initialize")

    def tearDown(self):
        self.testbed.deactivate()

    def test_save_recipe(self):
        self.rec_dao.save(self.rec2)
        self.assertEqual(Recipe.query().count(), 2)
        self.rec_dao.save(self.rec3)
        self.assertEqual(Recipe.query().count(), 3)
        self.assertIsInstance(Recipe.query().fetch()[0], Recipe)

    def test_get_recipe(self):
        r = self.rec_dao.get(self.rec1key.urlsafe())
        self.assertIsInstance(r, Recipe)
        self.assertEqual(r.name, u"Arroz con chícharos")

    def test_delete_recipe(self):
        self.rec_dao.delete(self.rec1.key.urlsafe())
        self.assertEqual(Recipe.query().count(), 0)

    def test_update_recipe(self):
        self.rec1.name = "Arroz tres delicias"
        self.rec1.category = Category(name="Comida china")
        self.rec1.steps = ["Facer algo", "Servir como queiras"]
        self.rec_dao.update(self.rec1)
        self.rec1 = Recipe.query().fetch()[0]
        self.assertEqual(self.rec1.name, "Arroz tres delicias")
        self.assertEqual(self.rec1.category.name, "Comida china")
        self.assertEqual(self.rec1.steps, ["Facer algo", "Servir como queiras"])

    def test_get_all(self):
        self.rec2.put()
        self.rec3.put()
        rec_list = self.rec_dao.get_all()
        self.assertEqual(len(rec_list), 3)
        self.assertIsInstance(rec_list[0], Recipe)
        self.assertEqual(rec_list[0].name, u"Arroz con chícharos")
        self.assertIsInstance(rec_list[1], Recipe)
        self.assertEqual(rec_list[1].name, u"Macarróns con tomate")
        self.assertIsInstance(rec_list[2], Recipe)
        self.assertEqual(rec_list[2].name, u"Gazpacho andaluz")

    def test_search(self):
        result_list = self.rec_dao.search("chí")
        self.assertTrue(self.rec1 in result_list)
        result_list = self.rec_dao.search("arroz")
        self.assertTrue(self.rec1 in result_list)
        self.rec2.put()
        result_list = self.rec_dao.search("macarróns")
        self.assertTrue(self.rec2 in result_list)
        result_list = self.rec_dao.search("pepperoni")
        self.assertFalse(self.rec1 in result_list)
        self.assertFalse(self.rec2 in result_list)




