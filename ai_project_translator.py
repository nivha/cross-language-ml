

afrom selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



driver = webdriver.Firefox()

driver.get("http://imtranslator.net/translation/english/to-spanish/translation/")
text = driver.find_element_by_name("source")
text.send_keys("school")
google_tab = driver.find_element_by_id("google")
t = google_tab.find_element_by_tag_name("span")
t.click()

#wait = ui.WebDriverWait(self.driver,10)
element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "tts2"))
    )
#wait.until(lambda driver: driver.title.lower().startswith('course details'))

target = driver.find_element_by_id("target")
translated = target.get_attribute("value")
print translated

driver.quit()


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
