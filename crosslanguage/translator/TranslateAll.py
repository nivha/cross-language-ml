import os
import time
from translator.FileTranslator import FileTranslator

os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'
from django.conf import settings

from crosslanguage.utils import Language
import shutil


__author__ = 'Ori'

class CategoryTranslator(object):
    """
    Translate a category in a source language to several target languages.
    """

    def _lang_to_wikipedia(self, lang):
        return {
            Language.English: 'en',
            Language.Spanish: 'es',
            Language.Hebrew: 'he',
        }[lang]

    def __init__(self, source_lang, target_lang_list, category_name):
        # Get path string for each language
        self.source_lang = source_lang
        self.source_lang_path = self._lang_to_wikipedia(source_lang)

        self.target_lang_list = target_lang_list
        self.target_lang_path_list = [self._lang_to_wikipedia(l) for l in target_lang_list]

        self.category_path = os.path.join(settings.DATA_DIR, self.source_lang_path, category_name)

    def do_translation(self):
        # First, remove folders with any translated content
        for folder in os.listdir(self.category_path):
            if folder in self.target_lang_path_list:
                shutil.rmtree(os.path.join(self.category_path, folder))

        # Then, translate all files for each language
        for target_lang in self.target_lang_list:
            target_lang_path = self._lang_to_wikipedia(target_lang)

            # Determine directory for translations
            target_path = os.path.join(self.category_path, target_lang_path)

            # Delete old folder of translations
            if os.path.isdir(target_path):
                shutil.rmtree(target_path)
                time.sleep(5)



            os.makedirs(target_path)

            # Make translator
            translator = FileTranslator(self.source_lang, target_lang)

            # Translate all files in directory
            for filename in os.listdir(self.category_path):
                if not filename.endswith('.txt'):
                    # Skip files which are not text files (ends with .txt)
                    continue
                file_source_path = os.path.join(self.category_path, filename)
                file_target_path = os.path.join(self.category_path, target_lang_path, filename)
                translator.translate_to_file(file_source_path, file_target_path)


def translate_all_lang_categoried(source_lang, targe_lang):
    pass


class DataTranslator(object):
    """
    Translates all data in the system
    """
    def __init__(self):
        pass


if __name__ == '__main__':
    tr = CategoryTranslator(Language.English, [Language.Spanish], 'Maxwell_Medal_and_Prize_recipients')
    tr.do_translation()

