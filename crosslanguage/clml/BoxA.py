
__author__ = 'Mojo'

import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'
from django.conf import settings

from clml.models import Category
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy

class Direction(object):
    Pre = 'pre'
    Post = 'post'


class SimpleClassifierTester(object):
    """
        bla bla..

        training_categories, testing_categories must be at the same length and organised such
        that each train_category are semantically same as the test_category at the same index
        i.e.:
            training_categories = ['Dark_matter', 'Black_holes']
            testing_categories  = ['Materia_oscura', 'Agujeros_negros']
    """

    def __init__(self, source_language, target_language, training_categories, testing_categories,
                 direction):
        self.source_language = source_language
        self.target_language = target_language
        self.training_categories = training_categories
        self.testing_categories = testing_categories
        self.direction = direction

        self.train_data = []
        self.train_target = []
        self.test_data = []
        self.test_target = []

        self._prepare_data()


    def _get_text(self, article):
        if self.direction == Direction.Pre:
            return article.articlecontent_set.get(language=self.source_language).text
        if self.direction == Direction.Post:
            return article.articlecontent_set.get(language=self.target_language).text

    def _prepare_data(self):
        """

        :return:
        """
        # acquire articles data and target for training
        for category in self.training_categories:
            for article in category.article_set.all():
                training_text = self._get_text(article)
                self.train_data.append(training_text)
                self.train_target.append(category.name)

        # acquire articles data and target for testing
        for i, category in enumerate(self.testing_categories):
            for article in category.article_set.all():
                testing_text = self._get_text(article)
                self.test_data.append(testing_text)
                self.test_target.append(training_categories[i].name)


    def _train(self):
        """

        :return:
        """
        # self.clf = Pipeline([('vect', CountVectorizer()),
        #                      ('tfidf', TfidfTransformer()),
        #                      ('clf', SGDClassifier(loss='hinge', penalty='l2',
        #                                            alpha=1e-3, n_iter=5)),
        #                      ])
        self.clf = Pipeline([('vect', CountVectorizer()),
                             ('tfidf', TfidfTransformer()),
                             ('clf', MultinomialNB()),
                             ])

        self.clf = self.clf.fit(self.train_data, self.train_target)

    def _test(self):
        predicted = self.clf.predict(self.test_data)
        score = numpy.mean(predicted == self.test_target)
        return score

    def score(self):

        self._prepare_data()
        self._train()
        score = self._test()
        return score



if __name__ == '__main__':
    training_categories = Category.objects.filter(language='en')
    testing_categories = Category.objects.filter(language='es')

    s = SimpleClassifierTester('en', 'es', training_categories, testing_categories, Direction.Pre)
    print s.score()