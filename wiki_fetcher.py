

import bs4
__import__("wikipedia")
__import__("wiki2plain")

from wikipedia import Wikipedia
from wiki2plain import Wiki2Plain


wiki = Wikipedia('en')
s = wiki.article('Volga_Germans')
s = Wiki2Plain(s)

