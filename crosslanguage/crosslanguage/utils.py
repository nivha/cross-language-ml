import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'
from crosslanguage import settings


class Language(object):
    """
    An all-purpose language object (sort of an ENUM).
    If you wish to add a language, add and update all following dicionaries.
    """
    English = 'English'
    Spanish = 'Spanish'
    Hebrew = 'Hebrew'

    # For each language, how it is represented in Wikipedia's URLs.
    # This is also the path of
    lang_to_path = {
        English: 'en',
        Spanish: 'es',
        Hebrew: 'he',
    }

    # This is how the language is represented in Google Translate URLs.
    lang_to_google_translate = {
        English: 'en',
        Spanish: 'es',
        Hebrew: 'iw',
    }

    def __init__(self, lang):
        self.lang = lang

    def to_path(self):
        return self.lang_to_path[self.lang]

    def to_google_translate(self):
        return self.lang_to_google_translate[self.lang]

    def __str__(self):
        return self.lang

    def __repr__(self):
        return str(self)



