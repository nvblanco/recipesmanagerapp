# coding: utf-8
__author__ = 'nico'

from entities import Category, Recipe, Ingredient


class Singleton(type):
    """
    Metaclass that restricts the instantiation of the subclass to one object
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def do_inserts():
    cat_arroces = Category(name="Arroces", description="Arrocitos")
    code = cat_arroces.put().urlsafe()
    cat_arroces.id = code
    cat_arroces.put()
    cat_pastas = Category(name="Pastas", description="Lorem ipsum")
    code = cat_pastas.put().urlsafe()
    cat_pastas.id = code
    cat_pastas.put()
    cat_sopas = Category(name="Sopas e cremas", description="Fresco, fresco")
    code = cat_sopas.put().urlsafe()
    cat_sopas.id = code
    cat_sopas.put()
    rec1 = Recipe(name="Arroz con chícharos",
                  category=cat_arroces,
                  servings=4,
                  ingredients=[Ingredient(name="Arroz", quantity="500gr"),
                               Ingredient(name="Chícharos", quantity="300gr")],
                  steps=["Cocemos o arroz", "Botámoslle os chícharos", "Servir en quente"])
    rec2 = Recipe(name="Macarróns con tomate",
                  category=cat_pastas,
                  servings=6,
                  ingredients=[Ingredient(name="Macarróns", quantity="600gr"),
                               Ingredient(name="Tomate frito", quantity="100gr")],
                  steps=["Cocemos os macarróns",
                         "Botámoslleo tomate frito",
                         "Servimos en quente"])
    rec3 = Recipe(name="Gazpacho andaluz",
                  category=cat_sopas,
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
    rec1.put()
    rec2.put()
    rec3.put()