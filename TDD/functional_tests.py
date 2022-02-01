from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Doris has heard about a cool new online to-do app. She goes
        # to check out it's homepage
        self.browser.get('http://localhost:8000')

        # She notices the page's header and title mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a To-Do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute(
            'placeholder'), 'Enter a to-do item')
        # She types "Buy a Gucci Bag" into a text box
        inputbox.send_keys('Buy a Gucci Bag')
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy a Gucci Bag" as an item in a To-Do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == '1: Buy a Gucci Bag' for row in rows))
        # There's still a textbox inviting her to add another item. She
        # enters "Pack church things into bag"
        self.fail('Finish the Test')
        # The page updates again, and now shows both items on her list
        # Doris wonders if the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.
        # She visits that URL - her to-do list is still there.
        # Satisfied, she goes back to sleep.


if __name__ == '__main__':
    unittest.main()
