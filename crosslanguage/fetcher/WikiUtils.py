# coding=utf-8
import os
import datetime
import re
import urllib
import lxml.etree



urlapi =  "http://en.wikipedia.org/w/api.php"




CATEGORY = {
    'en':   'Category',
    'es':   urllib.quote_plus('Categoría'),
}




# # needs also to handle redirects and marking up symbols and spaces
# def GetWikipediaPage(name):
#     "Downloads a single Wikipedia page and its metadata"
#     params = { "format":"xml", "action":"query", "prop":"revisions", "rvprop":"timestamp|user|comment|content" }
#     params["titles"] = "API|%s" % urllib.quote(name.encode("utf8"))
#     qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
#     url = "%s?%s" % (urlapi, qs)
#     tree = lxml.etree.parse(urllib.urlopen(url))
#     #print lxml.etree.tostring(tree.getroot())
#     normalizedname = name
#     normn = tree.xpath('//normalized/n')
#     if normn:
#         normalizedname = normn[0].attrib["to"]
#     revs = tree.xpath('//rev')
#     if len(revs) == 1:
#         return None
#     rev = revs[-1]
#     #print lxml.etree.tostring(rev)
#     return { "name":normalizedname, "text":rev.text,
#              "timestamp":rev.attrib.get("timestamp"),
#              "user":rev.attrib.get("user"), "comment":rev.attrib.get("comment") }


def GetWikipediaCategory(categoryname, language):
    "Downloads all/some names and metadata of pages in given category"

    params = {"action":"query", "format":"xml", "generator":"categorymembers", "prop":"info", "gcmlimit":100 }
    u"{:s}".format(CATEGORY[language])
    params["gcmtitle"] = u"{:s}:{:s}".format(CATEGORY[language], urllib.quote_plus(categoryname))
    result = [ ]
    while True:
        url = "%s?%s" % (urlapi, urllib.urlencode(params))
        tree = lxml.etree.parse(urllib.urlopen(url))
        for page in tree.xpath('//page'):
            pdata = dict(page.attrib.items())
            if "redirect" in pdata:   # case of the redirect page having a category, eg Paviland_Cave
                continue
            pdata.pop("new", None)
            assert set(['lastrevid', 'pageid', 'title', 'counter', 'length', 'touched', 'ns']).issubset(set(pdata.keys())), (pdata.keys(), pdata)
            pdata['length'] = int(pdata['length'])
            pdata['title'] = pdata['title'].encode('utf8')
            if pdata["title"][:5] == "File:":
                continue
            pdata['title_raw'] = urllib.quote(pdata["title"].replace(" ", "_"))
            pdata["link"] = "http://{:s}.wikipedia.org/wiki/{:s}".format(language, pdata['title_raw'])
            result.append(pdata)
        cmcontinue = tree.xpath('//query-continue/categorymembers') # attrib.get("gcmcontinue") is fed back in as gmcontinue parameter                     
        if not cmcontinue: 
            break
        params["gcmcontinue"] = cmcontinue[0].get("gcmcontinue")
    return result


def GetWikipediaCategoryRecurse(categoryname, language):
    "Downloads everything in a given category and all the subcategories"
    prestack = [ categoryname ]
    usedcategories = set()
    result = [ ]
    while prestack:
        lcategoryname = prestack.pop()
        if lcategoryname in usedcategories:
            continue
        for d in GetWikipediaCategory(lcategoryname, language):
            if d["title"][:9] == "{:s}:".format(CATEGORY[language]):
                prestack.append(d["title"][9:])
            else:
                result.append(d)
        usedcategories.add(lcategoryname)  # avoids infinite loops
    return result

        
# def ParseTemplates(text):
#     "Extract all the templates/infoboxes from the text into a list"
#     res = { "templates":[ ], "categories":[ ], "images":[ ], "wikilinks":[ ], "flattext":[ ] }
#     templstack = [ ]
#     for tt in re.split("(\{\{\{|\}\}\}|\{\{|\}\}|\[\[|\]\]|\|)", text):
#         if tt in ["{{{", "{{", "[["]:
#             templstack.append([tt, [ [ ] ] ])
#         elif templstack and tt in ["}}}", "}}", "]]"]:
#             templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
#             templstack[-1].append(tt)
#             if len(templstack) == 1:
#                 if templstack[-1][0] == "{{":
#                     ltempl = [ ]
#                     for i, param in enumerate(templstack[-1][1]):
#                         k, e, v = param.partition("=")
#                         if e:
#                             ltempl.append((k.strip(), v.strip()))
#                         else:
#                             ltempl.append((i, k.strip()))
#                     if ltempl:
#                         res["templates"].append((ltempl[0][1], dict(ltempl)))
#                 elif templstack[-1][0] == "[[":
#                     llink = templstack[-1][1]
#                     if llink:
#                         llink0, cllink, cllink1 = llink[0].partition(":")
#                         if llink[0][0] == ':':   # eg [[:Category:something]]
#                             res["wikilinks"].append(llink[-1])
#                             res["flattext"].append(llink[0][1:])  # the [[what you see|actual link]]
#                         elif cllink:
#                             if llink0 == "Category":
#                                 res["categories"].append(cllink1.strip())
#                             elif llink0 in ["Image", "File"]:
#                                 res["images"].append(cllink1.strip())
#                             elif len(llink0) == 2:
#                                 pass  # links to other languages
#                             else:
#                                 print "Unrecognized", llink
#                         else:
#                             res["wikilinks"].append(llink[-1])
#                             res["flattext"].append(llink[0])  # the [[what you see|actual link]]
#             else:
#                 templstack[-2][1][-1].append(templstack[-1][0])
#                 templstack[-2][1][-1].append("|".join(templstack[-1][1]))
#                 templstack[-2][1][-1].append(templstack[-1][2])
#             del templstack[-1]
#         elif tt == "|" and templstack:
#             templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
#             templstack[-1][1].append([ ])
#         elif templstack:
#             templstack[-1][1][-1].append(tt)
#         else:
#             res["flattext"].append(tt)
#     res["flattext"] = "".join(res["flattext"])
#     return res

#print GetWikipediaPage("Ireby Fell Cavern")
#print GetWikipediaPage("Category:Physics")
#print GetWikipediaCategory("Physics")
#print GetWikipediaCategoryRecurse("Physics")