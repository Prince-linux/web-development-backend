from selenium import webdriver
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
        self.fail('Finish the Test')


        # She is invited to enter a To-Do item straight away
        # She types "Buy a Gucci Bag" into a text box
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy a Gucci Bag" as an item in a To-Do list
        # There's still a textbox inviting her to add another item. She
        # enters "Pack church things into bag"
        # The page updates again, and now shows both items on her list
        # Doris wonders if the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.
        # She visits that URL - her to-do list is still there.
        # Satisfied, she goes back to sleep.
if __name__ == '__main__':
    unittest.main()
