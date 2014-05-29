# coding=utf-8
__author__ = 'niv'

from wikitools import wiki
from wikitools import category

# class CategoryFetcher(object):
#
#     def __init__(self, category, language='en'):
#         self.category = category
#         self.language = language
#
#     def fetch(self):
#


def get_category(category):
    return [article.title for article in category.getAllMembersGen()]

isCategory = lambda x: x[:len('Category')] == 'Category:'

def get_category_recursively(site, category_title):

    closed_categories = set()
    open_categories = [category_title]
    articles = set()

    while open:
        current_category = category.Category(site, open_categories.pop())

        for d in get_category(current_category):
            if d in closed_categories: continue
            if isCategory(d):
                #cat = category.Category(site, d)
                open_categories.append(cat)
            else:
                print d
                articles.add(d)
        closed_categories.add(current_category)

    return articles

site = wiki.Wiki()
cat = category.Category(site, "Category:Institute_of_Physics")
get_category_recursively(site, "Category:Institute_of_Physics")
#for article in cat.getAllMembersGen(): #namespaces=[0]
#    print article.urltitle


######### Spanish
# site = wiki.Wiki("http://es.wikipedia.org/w/api.php")
# cat = category.Category(site, "Categoría:Libros_de_física")
# for article in cat.getAllMembersGen(namespaces=[0]):
#     print article.urltitle
