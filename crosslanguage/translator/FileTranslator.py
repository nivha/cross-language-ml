import os

os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crosslanguage.utils import Language
import codecs
import traceback


# TODO: wrap the selenium with 'with'
class FileTranslator(object):

    def __init__(self, source_lang, target_lang):
        self.source_lang = source_lang
        self.target_lang = target_lang

    def translate_text(self, text_to_translate, quit_browser=True):
        try:
            # Initialize firefox driver
            driver = webdriver.Firefox()
            # Open Google Translate website
            url = "http://translate.google.com/#%s/%s/%s" % (self.source_lang.to_google_translate(),
                                                             self.target_lang.to_google_translate(),
                                                             text_to_translate)
            # print 'url: ' + url
            driver.get(url)

            # Wait for results to appear and retrive them
            result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "result_box")))
            translated_text = result.text

            return translated_text
        except Exception:
            print traceback.format_exc()
            print "="*50
        finally:
            # Quit no matter what
            if quit_browser:
                driver.quit()
                pass

    def translate_file(self, path):
        with open(path) as f:
            text = f.read()
            return self.translate_text(text)

    def translate_to_file(self, source_path, target_path):
        translated_text = self.translate_file(source_path)
        with codecs.open(target_path, 'w', 'utf-8') as f:
            f.write(translated_text)


if __name__ == '__main__':
    translator = FileTranslator(Language(Language.English), Language(Language.Spanish))
    source_path = os.path.join(settings.DATA_DIR, 'en', 'Maxwell_Medal_and_Prize_recipients', 'Artur_Ekert.txt')
    target_path = os.path.join(settings.DATA_DIR, 'en', 'Maxwell_Medal_and_Prize_recipients', 'es', 'Artur_Ekert.txt')

    translator.translate_to_file(source_path, target_path)




###
               # # Initialize firefox friver
            # driver = webdriver.Firefox()
            # # Open Google Translate website
            # driver.get("http://translate.google.com/")
            # # Select source language
            # driver.find_element_by_id("gt-sl-gms").click()
            # driver.find_element_by_xpath(r'//div[contains(text_to_translate(), "{0}") and @class="goog-menuitem-content"]'
            #                              .format(source_lang)).click()
            # # Select target language
            # driver.find_element_by_id("gt-tl-gms").click()
            # driver.find_elements_by_xpath(r'//div[contains(text_to_translate(), "{0}") and @class="goog-menuitem-content"]'
            #                               .format(target_lang))[1].click()
            #
            # # Write input into box
            # source = driver.find_element_by_id('source')
            # source.send_keys(text_to_translate)
            #
            # time.sleep(10)

###

    # print translate_text(source_lang, target_lang, text)

# driver = webdriver.Firefox()

# driver.get("http://imtranslator.net/translation/english/to-spanish/translation/")
# text = driver.find_element_by_name("source")
# text.send_keys("school")
# google_tab = driver.find_element_by_id("google")
# t = google_tab.find_element_by_tag_name("span")
# t.click()

# #wait = ui.WebDriverWait(self.driver,10)
# element = WebDriverWait(driver, 10).until(
        # EC.presence_of_element_located((By.ID, "tts2"))
# )
# #wait.until(lambda driver: driver.title.lower().startswith('course details'))

# target = driver.find_element_by_id("target")
# translated = target.get_attribute("value")
# print translated

# driver.quit()


##import mechanize
##
##class Element_by_id(object):
##    def __init__(self, id_text):
##        self.id_text = id_text
##    def __call__(self, f, *args, **kwargs):
##        return 'id' in f.attrs and f.attrs['id'] == self.id_text
##
##    
##
##b = mechanize.Browser()
##b.open("http://imtranslator.net/translation/english/to-spanish/translation/")
##b.select_form(nr=0)
##text = b.form.find_control(id="source")
##text = "work"
##
##s = b.response().read()
##f = open(r"C:\Users\niv\technion\bla.html", 'w')
##f.write(s)
##f.close()

