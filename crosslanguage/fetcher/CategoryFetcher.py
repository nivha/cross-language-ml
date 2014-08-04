# coding=utf-8
import urllib

__author__ = 'Niv & Ori'

from wikitools import wiki
from wikitools import category
from fetcher.utils import cat_lang

class CategoryFetcher(object):
    """
        :params
        @param language - relevant language of given wiki

        Code example:

            cf = CategoryFetcher('es')
            articles = cf.get_category_recursively('Categoría:Libros_de_ciencias_de_la_computación')
            for article in articles:
                print article

    """

    def __init__(self, language='en'):
        self.language = language

        # base_sites_by_language = {
        #     'en':   "https://en.wikipedia.org/w/api.php",
        #     'es':   "http://es.wikipedia.org/w/api.php"
        # }
        self.site_url = "https://{:s}.wikipedia.org/w/api.php".format(language)
        self.site = wiki.Wiki(self.site_url)


    def get_category_articles(self, category):
        return [article for article in category.getAllMembersGen()]

    def is_category(self, category):
        category_pattern = u'{:s}:'.format(cat_lang[self.language])
        return category[:len(category_pattern)] == category_pattern

    def attach_metadata(self, article):
        """ attaches the original url as an attribute """
        article.url = u"http://{:s}.wikipedia.org/wiki/".format(self.language) + article.urltitle
        return article

    def get_category_recursively(self, category_title, max_articles_num=None):
        """
        Iterative BFS on the category tree
        returns all articles found in the run, as wiki Page objects

        :param category_title: title of needed category
        :param max_articles_num: maximum number of articles to fetch. stops after reaching the limit
                                 'None' means without limit.
        :return:
        """

        closed_categories = set()
        open_categories = [category_title]
        articles = set()

        while open_categories:

            current_category_name = open_categories.pop()
            if current_category_name in closed_categories: continue
            current_category = category.Category(self.site, current_category_name)

            for d in self.get_category_articles(current_category):
                if self.is_category(d.title):
                    open_categories.append(d.title)
                else:
                    articles.add(self.attach_metadata(d))
                    # quit if maximum_articles_num reached
                    if max_articles_num is not None and len(articles) >= max_articles_num:
                        return articles
            closed_categories.add(current_category)

        return articles



######## English
# cf = CategoryFetcher('en')
# articles = cf.get_category_recursively("Category:Institute_of_Physics")
# for article in articles:
#    print article

######## Spanish
# cf = CategoryFetcher('es')
# articles = cf.get_category_recursively('Categoría:Libros_de_ciencias_de_la_computación')
# for article in articles:
#    print article

#articles = get_category_recursively(site, "Categoría:Libros_de_física")
