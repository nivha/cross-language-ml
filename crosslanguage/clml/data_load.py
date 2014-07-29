# coding=utf-8

import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'
from django.conf import settings

from clml.models import Category, Article, ArticleContent
from crosslanguage.utils import Language


def load_category(lang_path, category_path):
    """
    Load a category to the DB.
    Includes creating the category, loading the articles and all their translations.
    """

    cat_lang = {
        'en':   unicode('Category', 'utf-8'),
        'es':   unicode('Categoría', 'utf-8'),
    }

    # Resolve the category URL
    category_url = u'http://{:s}.wikipedia.org/wiki/{:s}:{:s}'.format(
        lang_path, cat_lang[lang_path], category_path)

    # Get path in
    path = os.path.join(settings.DATA_DIR, lang_path, category_path)
    print 'Loading category from path:', path

    # Create django category in database
    category = Category.objects.create(
        url=category_url,
        name=category_path,
        language=lang_path,
    )

    # Load all article in path directory.
    for filename in os.listdir(path):
        if os.path.isdir(os.path.join(path, filename)): continue
        # Exclude all non .txt files
        if not filename.endswith('.txt'):
            raise Exception('{:s} is not a txt file - what is it doing here?'.format(filename))

        with open(os.path.join(path, filename)) as f:
            text = f.read()
            title = os.path.splitext(filename)[0]
            article_url = 'http://{:s}.wikipedia.org/wiki/{:s}'.format(
                lang_path, title)

            article = Article.objects.create(
                category=category,
                url=article_url,
                title=title,
                original_language=lang_path,
                is_stub=False  # TODO - check in some way whether this is a stub
            )

            article_content = ArticleContent.objects.create(
                article=article,
                language=article.original_language,
                text=text,
            )

    # Load translations:
    for lang_dir in os.listdir(path):
        # Exclude all non directories
        if not os.path.isdir(os.path.join(path, lang_dir)):
            continue

        print 'lang_dir:', lang_dir

        # Load all article in path directory.
        for filename in os.listdir(os.path.join(path, lang_dir)):
            # Exclude all non .txt files
            if not filename.endswith('.txt'):
                continue

            with open(os.path.join(path, lang_dir, filename)) as f:
                text = f.read()
                article_url = 'http://'+lang_path+'.wikipedia.org/wiki/' + category_path

                # TODO: I delete here articles that appear twice (meaning that they appear in more than
                # TODO:   one category). This should be done somewhere else before..
                articles = Article.objects.filter(original_language=lang_path, title=os.path.splitext(filename)[0])
                if len(articles) != 1:
                    articles.delete()
                    continue
                article = articles[0]

                print 'adding ' + lang_dir + ' translation to ' + article.title + ' , originally in ' + lang_path
                article_content = ArticleContent.objects.create(
                    article=article,
                    language=lang_dir,
                    text=text,
                )


def load_language(lang_path):
    """
    Load all categories of a language, to the DB.
    """
    # lang = Language.path_to_lang[lang_path]
    for category_path in os.listdir(os.path.join(settings.DATA_DIR, lang_path)):
        load_category(lang_path, category_path)


def clean_all():
    """
    Cleans all DB..
    """
    Category.objects.all().delete()


if __name__ == '__main__':
    clean_all()

    load_language('en')
    load_language('es')





