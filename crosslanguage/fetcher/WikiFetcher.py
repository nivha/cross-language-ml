# coding=utf-8

import os
from wikitools import wiki
from fetcher.CategoryFetcher import CategoryFetcher

os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'
from django.conf import settings

import urllib

from wikipedia import Wikipedia as W_Orig
from wiki2plain import Wiki2Plain
#from WikiUtils import GetWikipediaCategoryRecurse



class FetcherError(Exception):
    pass


class WikiFetcher(object):
    """
        Fetch all articles in a Wikipedia Category
        Save each article to a file in the project's storage hierarchy
    """

    def __init__(self, category, language):
        self.category = category
        self.language = language
        self.category_base_dir = os.path.join(settings.DATA_DIR, self.language, urllib.quote_plus(self.category))

        sites_by_language = {
            'en':   ''
        }

        site = wiki.Wiki("http://es.wikipedia.org/w/api.php")


        self.articles = []

    def fetch_raw_articles(self):
        cf = CategoryFetcher(site, 'es')
        articles = cf.get_category_recursively('Categoría:Libros_de_ciencias_de_la_computación')
        self.articles = [article.urltitle for article in articles]

    def fetch_to_files(self):
        """
            Save all category's articles into files in the relevant place
        """
        if not os.path.exists(self.category_base_dir): os.makedirs(self.category_base_dir)

        # self.fetch_raw_articles()
        # for article in self.articles:
        #     path = os.path.join(self.category_base_dir, "{:s}.txt".format(article.title_raw))
        #     print path
        #     article.fetch()
        #     article.savetofile(path)

        from wikitools import wiki
        from wikitools import category
        site = wiki.Wiki()


        #site.login("username", "password")
        # Create object for "Category:Foo"
        cat = category.Category(site, self.category)
        # iterate through all the pages in ns 0
        for article in cat.getAllMembersGen():
            path = os.path.join(self.category_base_dir, "{:s}.txt".format(article.urltitle))
            print path
            text = article.getWikiText()
            with open(path, 'w') as f:
                f.write(text)


if __name__=="__main__":
    #c = CategoryFetcher("Maxwell_Medal_and_Prize_recipients", 'en')
    c = CategoryFetcher("Institute_of_Physics", 'en')
    #c = CategoryFetcher("Libros_de_física", 'es')
    c.fetch_to_files()






