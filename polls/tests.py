from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import os


class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        opts = Options()
        if os.getenv("CI"):
             opts.add_argument("-headless")
        cls.selenium = webdriver.Firefox(options=opts)
        cls.selenium.implicitly_wait(5)

        # Creem el superusuari
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_admin_login(self):

        self.selenium.get(f"{self.live_server_url}/admin/")

        # Introduïm les credencials
        self.selenium.find_element(By.NAME, "username").send_keys("isard")

        self.selenium.find_element(By.NAME, "password").send_keys("pirineus")

        self.selenium.find_element(By.XPATH, "//input[@type='submit']").click()

        # Comprovem que hem iniciat sessió
        self.assertEqual( self.selenium.title , "Site administration | Django site admin" )
        # Cliquem link Questions
        self.selenium.find_element(By.LINK_TEXT, "Questions").click()
        # Comprovem que hem entrat a Questions
        self.assertEqual(self.selenium.title, "Select question to change | Django site admin")

        # Cliquem Add question
        self.selenium.find_element(By.XPATH, "//a[contains(text(), 'Add question')]").click()
        # Comprovem que estem  a  Add question
        self.assertEqual(self.selenium.title, "Add question | Django site admin")
        # Introduïm el text de la pregunta
        self.selenium.find_element(By.ID, "id_question_text").send_keys("Quin sistema operatiu de movil prefereixes?")
        # Cliquem link Today i Now
        self.selenium.find_element(By.LINK_TEXT, "Today").click()
        self.selenium.find_element(By.LINK_TEXT, "Now").click()
	# Guardem  i afegim un altre
        self.selenium.find_element(By.NAME, "_addanother").click()

        # Introduïm el text de la 2 pregunta
        self.selenium.find_element(By.ID, "id_question_text").send_keys("Quina marca prefereixes iphone o samsung?")
        # Cliquem link Today i Now
        self.selenium.find_element(By.LINK_TEXT, "Today").click()
        self.selenium.find_element(By.LINK_TEXT, "Now").click()
        # Guardem
        self.selenium.find_element(By.NAME, "_save").click()

	# Comprovem que hem tornat al llistat de Questions
        self.assertEqual(self.selenium.title, "Select question to change | Django site admin")
        #Cliquem en Choices
        self.selenium.find_element(By.LINK_TEXT, "Choices").click()
        # Cliquem Add choice
        self.selenium.find_element(By.XPATH, "//a[contains(text(), 'Add choice')]").click()

        # Seleccionem la pregunta
        Select(self.selenium.find_element(By.ID, "id_question")).select_by_value("1")
        self.selenium.find_element(By.ID, "id_choice_text").send_keys("IOS")

        # Guardem  i afegim un altre
        self.selenium.find_element(By.NAME, "_addanother").click()

        # Seleccionem la pregunta
        Select(self.selenium.find_element(By.ID, "id_question")).select_by_value("1")
        self.selenium.find_element(By.ID, "id_choice_text").send_keys("Android")

        # Guardem  i afegim un altre
        self.selenium.find_element(By.NAME, "_addanother").click()

        # Seleccionem la pregunta
        Select(self.selenium.find_element(By.ID, "id_question")).select_by_value("2")
        self.selenium.find_element(By.ID, "id_choice_text").send_keys("IPHONE")

        # Guardem  i afegim un altre
        self.selenium.find_element(By.NAME, "_addanother").click()

        # Seleccionem la pregunta
        Select(self.selenium.find_element(By.ID, "id_question")).select_by_value("2")
        self.selenium.find_element(By.ID, "id_choice_text").send_keys("SAMSUNG")

        # Guardem
        self.selenium.find_element(By.NAME, "_save").click()


        # Comprovem que hem tornat
        self.assertEqual(self.selenium.title, "Select choice to change | Django site admin")

        # Cliquem en Questions
        self.selenium.find_element(By.XPATH, "//a[contains(text(), 'Questions')]").click()

        # Comprovem que estem questions
        self.assertEqual(self.selenium.title, "Select question to change | Django site admin")

        # Accedim a la pregunta mitjançant l'URL
        self.selenium.find_element(By.XPATH, "//a[@href='/admin/polls/question/1/change/']").click()

        self.assertEqual(self.selenium.find_element(By.ID, "id_choice_set-0-choice_text").get_attribute("value"), "IOS")

        self.assertEqual(self.selenium.find_element(By.ID, "id_choice_set-1-choice_text").get_attribute("value"), "Android")


	# Guardem
        self.selenium.find_element(By.NAME, "_save").click()

        # Accedim a la pregunta mitjançant l'URL
        self.selenium.find_element(By.XPATH, "//a[@href='/admin/polls/question/2/change/']").click()

        self.assertEqual(self.selenium.find_element(By.ID, "id_choice_set-0-choice_text").get_attribute("value"), "IPHONE")

        self.assertEqual(self.selenium.find_element(By.ID, "id_choice_set-1-choice_text").get_attribute("value"), "SAMSUNG")

        # Guardem
        self.selenium.find_element(By.NAME, "_save").click()



