# coding=utf-8
__author__ = 'niv'

from wikitools import wiki
from wikitools import category

site = wiki.Wiki()


cat = category.Category(site, "Institute_of_Physics")
#for article in cat.getAllMembersGen(): #namespaces=[0]
    #print article.urltitle
print cat.getCategories()


# closed = set()
# open = [i.urltitle for i in cat.getAllMembers(namespaces=[0])]
# while open:
#     current = open.pop()
#     if isCategory(current):
#         new_category_name = current[current.find('%3A')+1:]
#         new_category = category.Category(site, new_category_name)
#         titles = new_category.getAllMembers()

# site = wiki.Wiki("http://es.wikipedia.org/w/api.php")
# cat = category.Category(site, "Libros_de_física")
# for article in cat.getAllMembersGen(namespaces=[0]):
#     print article.urltitle
