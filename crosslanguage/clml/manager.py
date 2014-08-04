import os
from clml.cleaner import clean_untranslated_articels

from clml.data_load import load_category
from clml.utils import get_category_folder


__author__ = 'Niv & Ori'


def download_cateogries(language, categories, max_articles_num):

    # for category in categories:
    #     wf = WikiFetcher(language, category, max_articles_num)
    #     wf.fetch_to_files()

    # for c in es_categories:
    #     tr = CategoryTranslator(Language(Language.Spanish), [Language(Language.English)], c)
    #     tr.do_translation()
    pass



en_categories = ['Asian_art', 'Latin_American_art']
es_categories = ['Arte_de_Asia', 'Arte_latinoamericano']

for c in en_categories:
    clean_untranslated_articels('en', c)
    load_category('en', c)
for c in es_categories:
    clean_untranslated_articels('es', c)
    load_category('es', c)
