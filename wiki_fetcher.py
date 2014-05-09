

import bs4
__import__("wikipedia")
__import__("wiki2plain")

__import__("wikipedia_utils_julian_todd")

from wikipedia import Wikipedia
from wiki2plain import Wiki2Plain
from wikipedia_utils_julian_todd import GetWikipediaCategoryRecurse, GetWikipediaCategory

# wiki = Wikipedia('en')
# s = wiki.article('Volga_Germans')
# s = Wiki2Plain(s)
# print s

l= GetWikipediaCategoryRecurse("Institute_of_Physics")
pass


