import os
import pathlib
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By

# Browser testing by Selenium

def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()

# The driver to simulate the test cases on (in this case its Chrome)
# Good for testing if the features work in other browsers too (such as Firefox)
driver = webdriver.Chrome()

# A class which defines which Tests I would want to run on my webpage
class WebpageTests(unittest.TestCase):

    def test_title(self):
        driver.get(file_uri("counter.html"))
        self.assertEqual(driver.title, "Counter")

    def test_increase(self):
        # Get the html page first, to simulate in Chrome
        driver.get(file_uri("counter.html"))

        # Get the increase button in the html page
        increase = driver.find_element(by=By.ID, value="increase")

        # Simulate a click
        increase.click()

        # Access the text in the element with id="h1", test if its equal to 1
        self.assertEqual(driver.find_element(by=By.ID, value="number").text, "1")

    def test_decrease(self):
        driver.get(file_uri("counter.html"))
        decrease = driver.find_element(by=By.ID, value="decrease")
        decrease.click()
        self.assertEqual(driver.find_element(by=By.ID, value="number").text, "-1")


