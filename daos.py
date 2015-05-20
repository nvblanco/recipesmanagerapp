__author__ = 'nico'

import unicodedata
import sys

from google.appengine.ext import ndb

from entities import Recipe, Category


class GenericDAO(object):
    related_class = None

    def get(self, code):
        """
        Obtains an object by his code
        @param code: The code, in a url-safe way.
        @return: Retrieved object.
        """
        key = ndb.Key(urlsafe=code)
        return key.get()

    def update(self, r):
        """
        Update an object in datastore
        @param r: The object
        """
        r.put()

    def delete(self, code):
        """
        Delete an object by code
        @param code: The code, in a urlsafe-way
        """
        key = ndb.Key(urlsafe=code)
        key.delete()

    @classmethod
    def get_all(cls):
        """
        Retrieves all elements of a giving type
        @return: List with all elements of a giving type
        """
        return cls.related_class.query().fetch()


class RecipeDAO(GenericDAO):
    """
    Class that performs CRUD operations over Recipe objects
    """
    related_class = Recipe

    def save(self, r):
        """
        Saves Category object in Datastore
        @param r: The object
        @return: The code of the object, in a urlsafe-way
        """
        return r.put().urlsafe()

    @staticmethod
    def search(chain):
        """
        Method that obtains all recipes that contain
        the string passed as parameter in the name attribute.
        @param chain: The search string.
        @return: List of recipes that match with the search string.
        """
        reload(sys)
        sys.setdefaultencoding("utf-8")

        def normalize(input_str):
            """
            Removes accents of a string.
            @param input_str: Original string.
            @return: Same string with all accents removed.
            """
            input_str = input_str.lower()
            nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
            return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

        return [r for r in Recipe.query() if normalize(chain) in normalize(r.name)]

    def get_by_category(self, cat_code):
        """
        Obtains all category recipes.
        @param cat_code: Code of category, in a urlsafe-way.
        @return: List of category recipes.
        """
        return [r for r in self.get_all() if r.category.id == CategoryDAO().get(cat_code).key.urlsafe()]


class CategoryDAO(GenericDAO):
    """
    Class that performs CRUD operations over Category objects
    """

    related_class = Category

    def save(self, r):
        """
        Saves Category object in Datastore
        @param r: The object
        @return: The code of the object, in a urlsafe-way
        """
        code = r.put().urlsafe()
        r = self.get(code)
        r.id = code
        self.update(r)
        return code

    def get_by_name(self, name):
        """
        Obtains a category by name.
        @param name: Name of category.
        @return: Category object.
        """
        return Category.query(Category.name == name).fetch()[0]