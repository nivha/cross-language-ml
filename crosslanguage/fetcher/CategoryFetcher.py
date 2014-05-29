# coding=utf-8
__author__ = 'niv'

from wikitools import wiki
from wikitools import category

class CategoryFetcher(object):
    """
        :params
        @param site - a wiki site
        @param language - relevant language of given wiki

        Code example:

            site = wiki.Wiki("http://es.wikipedia.org/w/api.php")
            cf = CategoryFetcher(site, 'es')
            articles = cf.get_category_recursively('Categoría:Libros_de_ciencias_de_la_computación')
            for article in articles:
                print article

    """

    def __init__(self, site, language='en'):
        self.site = site
        self.language = language

    def get_category(self, category):
        return [article for article in category.getAllMembersGen()]


    def is_category(self, category):
        cat_lang = {
            'en':   unicode('Category', 'utf-8'),
            'es':   unicode('Categoría', 'utf-8'),
        }
        category_pattern = u'{:s}:'.format(cat_lang[self.language])
        return category[:len(category_pattern)] == category_pattern

    def get_category_recursively(self, category_title):
        """
            Iterative BFS on the category tree
            returns all articles found in the run, as wiki Page objects
        """

        closed_categories = set()
        open_categories = [category_title]
        articles = set()

        while open_categories:

            current_category_name = open_categories.pop()
            if current_category_name in closed_categories: continue
            current_category = category.Category(self.site, current_category_name)

            for d in self.get_category(current_category):
                if self.is_category(d.title):
                    open_categories.append(d.title)
                else:
                    articles.add(d)
            closed_categories.add(current_category)

        return articles



######## English
# site = wiki.Wiki()
# cf = CategoryFetcher(site, 'en')
# articles = cf.get_category_recursively("Category:Institute_of_Physics")
# for article in articles:
#    print article

######## Spanish
# site = wiki.Wiki("http://es.wikipedia.org/w/api.php")
# cf = CategoryFetcher(site, 'es')
# articles = cf.get_category_recursively('Categoría:Libros_de_ciencias_de_la_computación')
# for article in articles:
#    print article

#articles = get_category_recursively(site, "Categoría:Libros_de_física")
