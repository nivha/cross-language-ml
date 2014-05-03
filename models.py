



class Cateogry:
    url = Charfield
    name = Charfield
    language = Charfield
    
        
class Article(Modles.model):
    catergory = FK(Cateigory)
    url = charfield
    name = charfield
    original_language = charfield
   
class ArticleContent(Article):
    article = FK(Article)
    language = charfield
    
    text = models.TextField()
     
     
     
