__author__ = 'Mojo'

import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'
from django.conf import settings

from clml.models import Category, Article


class SimpleClassifierTester(object):

    def __init__(self, source_language, target_language, training_categories, testing_categories):
        self.source_language     = source_language
        self.target_language     = target_language
        self.training_categories = training_categories
        self.testing_categories  = testing_categories


    def _prepare_data(self):
        """

        :return:
        """

        data = []
        target = []


        # acquire articles data and target
        for category in self.training_categories:
            print category

    def _train(self):
        """

        :return:
        """
        pass

    def _test(self):
        pass

    def score(self):

        self._prepare_data()
        # self._train()
        # score = self._test()
        # return score


if __name__ == '__main__':
    c = Category.objects.all()

    # s = SimpleClassifierTester('es', 'en', )
