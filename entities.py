# coding=utf-8
__author__ = 'nico'

from google.appengine.ext import ndb


class Category(ndb.Model):
    id = ndb.StringProperty()
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    image = ndb.BlobProperty()


class Ingredient(ndb.Model):
    name = ndb.StringProperty()
    quantity = ndb.StringProperty()


class Recipe(ndb.Model):
    name = ndb.StringProperty(required=True)
    category = ndb.StructuredProperty(Category, required=True)
    servings = ndb.IntegerProperty(required=True)
    ingredients = ndb.StructuredProperty(Ingredient, repeated=True)
    steps = ndb.StringProperty(repeated=True)
    image = ndb.BlobProperty()


