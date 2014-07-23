# coding=utf-8

import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'

from django.conf import settings
from fetcher.CategoryFetcher import CategoryFetcher
import urllib
from wiki2plain import Wiki2Plain
#from wikipedia import Wikipedia as W_Orig
#from wiki2plain import Wiki2Plain
#from WikiUtils import GetWikipediaCategoryRecurse



class FetcherError(Exception):
    pass


class WikiFetcher(object):
    """
        Fetch all articles in a Wikipedia Category
        Save each article to a file in the project's storage hierarchy
    """

    def __init__(self, language, category):
        self.category = category
        self.language = language

        self.category_base_dir = os.path.join(settings.DATA_DIR, self.language, urllib.quote_plus(self.category))
        #self.articles = []

    def fetch_raw_articles(self):
        cf = CategoryFetcher(self.language)
        return cf.get_category_recursively(self.category)
        #self.articles = [article.urltitle for article in articles]

    def fetch_to_files(self):
        """
            Save all category's articles into files in the relevant place
        """
        if not os.path.exists(self.category_base_dir): os.makedirs(self.category_base_dir)

        articles = self.fetch_raw_articles()
        for article in articles:
            path = os.path.join(self.category_base_dir, "{:s}.txt".format(urllib.quote_plus(article.urltitle)))
            print path
            raw_text = article.getWikiText()
            # clean text - leave only wiki text
            clean_text = Wiki2Plain(raw_text).text
            with open(path, 'w') as f:
                f.write(clean_text)


if __name__=="__main__":

    # #c = CategoryFetcher("Maxwell_Medal_and_Prize_recipients", 'en')
    # c = CategoryFetcher("Institute_of_Physics", 'en')
    # #c = CategoryFetcher("Libros_de_física", 'es')
    # c.fetch_to_files()

    # wf = WikiFetcher('en', "Institute_of_Physics")
    # wf = WikiFetcher('en', "International_Young_Physicists'_Tournament")
    wf = WikiFetcher('es', "Libros_de_ciencias_de_la_computación")

    wf.fetch_to_files()







