# coding=utf-8
__author__ = 'nico'

import unittest

from google.appengine.ext import testbed

from entities import Category
from daos import CategoryDAO


class CategoryDAOTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        self.cat_dao = CategoryDAO()

        self.cat_arroces = Category(name="Arroces", description="Arrocitos")
        self.cat_sopas = Category(name="Sopas e cremas", description="Categoria chula")
        self.cat_pastas = Category(name="Pastas", description="Fresco, fresco")

        self.cat_arroces_key = self.cat_arroces.put()
        self.assertEqual(Category.query().count(), 1, "Failed to initialize test")

    def tearDown(self):
        self.testbed.deactivate()

    def test_save_category(self):
        self.cat_dao.save(self.cat_sopas)
        self.assertEqual(Category.query().count(), 2)
        self.cat_dao.save(self.cat_pastas)
        self.assertEqual(Category.query().count(), 3)
        self.assertIsInstance(Category.query().fetch()[0], Category)

    def test_get_category(self):
        r = self.cat_dao.get(self.cat_arroces_key.urlsafe())
        self.assertIsInstance(r, Category)
        self.assertEqual(r.name, u"Arroces")

    def test_delete_category(self):
        self.cat_dao.delete(self.cat_arroces.key.urlsafe())
        num_categories = Category.query().count()
        self.assertEqual(num_categories, 0)

    def test_update_category(self):
        self.cat_arroces.name = "Arrocines"
        self.cat_dao.update(self.cat_arroces)
        self.cat_arroces = Category.query().fetch()[0]
        self.assertEqual(self.cat_arroces.name, "Arrocines")

    def test_get_all(self):
        self.cat_pastas.put()
        self.cat_sopas.put()
        cat_list = self.cat_dao.get_all()
        self.assertEqual(len(cat_list), 3)
        self.assertIsInstance(cat_list[0], Category)
        self.assertEqual(cat_list[0].name, u"Arroces")
        self.assertIsInstance(cat_list[1], Category)
        self.assertEqual(cat_list[1].name, u"Pastas")
        self.assertIsInstance(cat_list[2], Category)
        self.assertEqual(cat_list[2].name, u"Sopas e cremas")

