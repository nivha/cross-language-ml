import string
from selenium import webdriver
import time
from selenium.webdriver.remote.webelement import WebElement
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def translate_text(source_lang, target_lang, text_to_translate, quit_browser=True):
    try:
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

        # Initialize firefox driver
        driver = webdriver.Firefox()
        # Open Google Translate website
        url = "http://translate.google.com/#%s/%s/%s" % (source_lang, target_lang, text_to_translate)
        # print 'url: ' + url
        driver.get(url)

        # Wait for results to appear and retrive them
        result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "result_box")))
        translated_text = result.text

        return translated_text
    finally:
        # Quit no matter what
        if quit_browser:
            driver.quit()
        pass


if __name__ == '__main__':
    text = """Oxbow (foaled March 26, 2010), an American Thoroughbred racehorse, is best known for winning the second jewel in the United States Triple Crown of Thoroughbred Racing, the 2013 Preakness Stakes. A bay colt who was sired by a winner of the Breeders' Cup Classic and out of a full sister to another Breeders' Cup Classic winner, Oxbow was sold as a yearling at Keeneland for $250,000 and is owned by Brad Kelley of Calumet Farm. He was trained by D. Wayne Lukas and was ridden in his Triple Crown races by Gary Stevens. Oxbow had a reputation as a front-runner who was difficult to rate during his races. Plagued with frequent turnover in jockeys prior to the Triple Crown series, and often running from poor starting gate post positions, he had only two wins prior to his victory in the Preakness. That success was Calumet Farm's first win in a Triple Crown race in 45 years and breeder Richard Santulli's first win in a Triple Crown classic race. It also was Stevens' first Triple Crown win since 2001, following his return to riding in early 2013 after a seven-year retirement, and Lukas' first Triple Crown win since 2000. Oxbow's second-place finish in the Belmont Stakes in June made him the third horse that year to reach $1 million in purse wins. Following the Belmont, he was ranked the top three-year-old racehorse in the United States by the National Thoroughbred Racing Association (NTRA). He was pulled up shortly after finishing fourth in the Haskell Invitational, and was found to have suffered a soft tissue injury, was taken out of competition for the remainder of his three-year-old season, and retired in October 2013. He stands at stud for the 2014 breeding season at Taylor Made Stallions in Lexington, Kentucky."""
    # text = """stupid dog"""
    print '>>>>>>>>>>>'
    result = translate_text('en', 'es', text, quit_browser=False)
    fixed_result = filter(lambda x: x in string.printable, result)  # TODO: fix bad characters such as e' and a' and e^ in spanish
    print fixed_result
    print '<<<<<<<<<<<'



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
