# coding=utf-8

import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'

from django.conf import settings
from fetcher.CategoryFetcher import CategoryFetcher
import urllib
from wiki2plain import Wiki2Plain

class FetcherError(Exception):
    pass


class WikiFetcher(object):
    """
        Fetch all articles in a Wikipedia Category
        Save each article to a file in the project's storage hierarchy

        Code example:

            # wf = WikiFetcher('en', "Institute_of_Physics")
            # wf = WikiFetcher('en', "International_Young_Physicists'_Tournament")
            wf = WikiFetcher('es', "Libros_de_ciencias_de_la_computación")
            wf.fetch_to_files()
    """

    def __init__(self, language, category, max_articles_num=None):
        self.category = category
        self.language = language
        self.max_articles_num = max_articles_num

        self.category_base_dir = os.path.join(settings.DATA_DIR, self.language, urllib.quote_plus(self.category))

    def fetch_raw_articles(self):
        cf = CategoryFetcher(self.language)
        return cf.get_category_recursively(self.category, self.max_articles_num)

    def fetch_to_files(self):
        """
            Save all category's articles into files in the relevant place
        """
        if not os.path.exists(self.category_base_dir): os.makedirs(self.category_base_dir)

        articles = self.fetch_raw_articles()
        print 'Fetched {:d} articles'.format(len(articles))
        for article in articles:
            article_title = urllib.quote_plus(article.urltitle)
            path = os.path.join(self.category_base_dir, "{:s}.txt".format(article_title))
            print path
            raw_text = article.getWikiText()
            raw_text = unicode(raw_text, 'utf-8')

            # clean text - leave only wiki text
            clean_text = Wiki2Plain(raw_text, self.language).text
            clean_text = clean_text.encode('utf8')

            with open(path, "w") as f:
                f.write(clean_text)


if __name__=="__main__":

    # wf = WikiFetcher('en', "Institute_of_Physics")
    # wf = WikiFetcher('en', "International_Young_Physicists'_Tournament")
    # wf = WikiFetcher('es', "Libros_de_ciencias_de_la_computación")
    # wf = WikiFetcher('es', "Sistemas_de_gestión_empresarial_libres")
    # wf = WikiFetcher('en', "Aetobatus")

    # some real shit now:
    # en_categories = ['Dark_matter', 'Black_holes']
    # es_categories = ['Materia oscura', 'Agujeros negros']

    en_categories = ['Asian_art', 'Latin_American_art']
    es_categories = ['Arte_de_Asia', 'Arte_latinoamericano']

    # for category in en_categories:
    #     wf = WikiFetcher('en', category, 200)
    #     wf.fetch_to_files()
    for category in es_categories:
        wf = WikiFetcher('es', category, 200)
        wf.fetch_to_files()







