import os
import simplejson
from clml.utils import get_category_folder

__author__ = 'Mojo'



def clean_english_articles_with_spanish_parallels(en_category_name, es_category_name):
    en_folder = get_category_folder('en', en_category_name)
    es_folder = get_category_folder('es', es_category_name)

    # collect original spanish urls from spanish category
    es_urls = set()
    for fname in os.listdir(es_folder):
        p = os.path.join(es_folder, fname)
        with open(p) as f:
            d = simplejson.loads(f.read())
            es_urls.add(d['original_url'])

    to_delete = []
    for fname in os.listdir(en_folder):
        p = os.path.join(en_folder, fname)
        with open(p) as f:
            d = simplejson.loads(f.read())
            if d['spanish_url'] in es_urls:
                to_delete.append(p)

    # delete them!
    for path in to_delete:
        print 'removing', path
        os.remove(path)


clean_english_articles_with_spanish_parallels('Black_holes', 'Agujeros_negros')
clean_english_articles_with_spanish_parallels('Dark_matter', 'Materia_oscura')

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
