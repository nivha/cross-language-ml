import os

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


def clean_untranslated_articels(language, category_name):
    # clean articles that counldn't be translated

    category_path = get_category_folder(language, category_name)
    other_lang = 'es' if language == 'en' else 'en'
    # get original language files
    orig = set(filter(lambda x: os.path.splitext(x)[-1]=='.txt', os.listdir(category_path)))
    trans = set(filter(lambda x: os.path.splitext(x)[-1]=='.txt', os.listdir(os.path.join(category_path, other_lang))))

    untranslated = orig - trans
    # delete untranslated
    for fname in untranslated:
        path = os.path.join(category_path, fname)
        print 'deleting', path
        os.remove(path)


en_categories = ['Asian_art', 'Latin_American_art']
es_categories = ['Arte_de_Asia', 'Arte_latinoamericano']

for c in en_categories:
    clean_untranslated_articels('en', c)
    load_category('en', c)
for c in es_categories:
    clean_untranslated_articels('es', c)
    load_category('es', c)
