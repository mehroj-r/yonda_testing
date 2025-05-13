import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from BasePageTest import BasePageTest


class SearchPageTest(BasePageTest):

    SEARCH_URL = "https://yonda.uz/search"
    active_navigation_idx = 0
    skip_footer = True

    def test_01_search_desktop(self):
        """Test the functionality of Search in left side. [DESKTOP]"""

        # Test for 'search-left'
        search_left = self.driver.find_element(By.XPATH, "//div[@class='search-left']")
        self.assertTrue(search_left.is_displayed(), "Search left side should be visible")

        # Test for 'search-right'
        search_right = self.driver.find_element(By.XPATH, "//div[@class='search-right']")
        self.assertTrue(search_right.is_displayed(), "Search right side should be visible")

        # Test for 'Ro`yxatni ko`rsatish' button
        show_list_btn = search_left.find_element(By.XPATH, "//button[contains(text(), 'Ro`yxatni ko`rsatish')]")
        self.assertFalse(show_list_btn.is_displayed(), "'Ro`yxatni ko`rsatish' button should not be visible")

        # Test for 'Kategoriya tanlang' button
        category_btn = search_left.find_element(By.XPATH, "//div[@class='sidebar-input-group']/child::div[@class='select-input']//div[@class='select-content']")
        self.assertTrue(category_btn.is_displayed(), "'Kategoriya tanlang' button should be visible")

        # Wait for 'search-cards' to get loaded
        self.wait.until(lambda d: len(d.find_elements(By.XPATH, "//div[@class='search-left']//div[@class='search-card-wrapper desktop-only']//div[@class='search-card']")) > 0)

        # Test for 'search-cards' button
        search_cards = search_left.find_elements(By.XPATH, "//div[@class='search-card-wrapper desktop-only']//div[@class='search-card']")
        self.assertGreater(len(search_cards), 0, "Search card count should be more than 0.")

    def test_02_searchbox(self):
        """Test the functionality of Search. [DESKTOP]"""

        # Test for 'search-left'
        search_left = self.driver.find_element(By.XPATH, "//div[@class='search-left']")
        self.assertTrue(search_left.is_displayed(), "Search left side should be visible")

        # Test for 'searchbox'
        searchbox = self.driver.find_element(By.XPATH, "//div[@class='search-left']//input[@id='search']")
        self.assertTrue(searchbox.is_displayed(), "Search box should be visible")

        # Click 'searchbox' to focus
        self.wait.until(EC.element_to_be_clickable(searchbox))
        self.driver.execute_script("arguments[0].click();", searchbox)

        # Type some something to 'searchbox'
        test_words = ["cambridge", "turon", "edu", "class"]

        for word in test_words:

            searchbox.clear()
            searchbox.send_keys(word)
            searchbox.send_keys(Keys.ENTER)

            # Wait for stuff to get fetched
            time.sleep(1)

            # Wait for 'search-cards' to get loaded
            self.wait.until(lambda d: len(d.find_elements(By.XPATH, "//div[@class='search-left']//div[@class='search-card-wrapper desktop-only']//div[@class='search-card']")) > 0)

            # Test for 'search-card' titles
            card_titles = search_left.find_elements(By.XPATH, "//div[@class='search-card-wrapper desktop-only']/child::div[@class='search-card-inner']//div[@class='search-card']")
            for card_title in card_titles:
                self.assertTrue(word in card_title.text.lower() , f"Should get correct results: {card_title.text}")

    def test_03_category(self):
        """Test the functionality of Search. [DESKTOP]"""

        # Test for 'search-left'
        search_left = self.driver.find_element(By.XPATH, "//div[@class='search-left']")
        self.assertTrue(search_left.is_displayed(), "Search left side should be visible")

        # Test for 'Kategoriya tanlang' button
        category_btn = search_left.find_element(By.XPATH, "//div[@class='sidebar-input-group']/child::div[@class='select-input']//div[@class='select-content']")
        self.assertTrue(category_btn.is_displayed(), "'Kategoriya tanlang' button should be visible")

        # Wait for the dropdown to appear
        dropdown_options = category_btn.find_elements(By.XPATH, "//div[@class='sidebar-input-group']/child::div[@class='select-input']//div[@class='select-content']//div[@class='select-options ']//div[@class='option ']//div[@class='left']/child::div")

        for option in dropdown_options:
            self.assertFalse(option.is_displayed(), "Option should not be visible")

        # Click the button
        category_btn.click()
        time.sleep(0.5)

        for option in dropdown_options:
            self.assertTrue(option.is_displayed(), "Option should be visible")

        # Expected categories
        expected_categories = ["IT", "Sport", "San'at", "Ta'lim", "Repetitor"]
        actual_categories = [option.text for option in dropdown_options]
        self.assertEqual(sorted(expected_categories), sorted(actual_categories), "Categories should be the same")

        # Close dropdown
        category_btn.click()
        time.sleep(0.5)

    def test_04_logic_correct_cases(self):
        """Test the functionality of Search by correct category."""

        # Test for 'search-left'
        search_left = self.driver.find_element(By.XPATH, "//div[@class='search-left']")
        self.assertTrue(search_left.is_displayed(), "Search left side should be visible")

        # Test for 'Kategoriya tanlang' button
        category_btn = search_left.find_element(By.XPATH, "//div[@class='sidebar-input-group']/child::div[@class='select-input']//div[@class='select-content']")
        self.assertTrue(category_btn.is_displayed(), "'Kategoriya tanlang' button should be visible")

        # Test for 'searchbox'
        searchbox = self.driver.find_element(By.XPATH, "//div[@class='search-left']//input[@id='search']")
        self.assertTrue(searchbox.is_displayed(), "Search box should be visible")

        # Wait for the dropdown to appear
        dropdown_options = category_btn.find_elements(By.XPATH, "//div[@class='sidebar-input-group']/child::div[@class='select-input']//div[@class='select-content']//div[@class='select-options ']//div[@class='option ']//div[@class='left']/child::div")

        test_cases = [
            {
                "category": 0,
                "name": 'Forward Academy',
            },
            {
                "category": 2,
                "name": '"Everest" o\'quv markazi, Parkentskiy filiali',
            },
            {
                "category": 4,
                "name": 'Python Teacher',
            }
        ]

        for test_case in test_cases:
            # Type into searchbox
            word = test_case["name"]

            searchbox.clear()
            searchbox.send_keys(word)
            searchbox.send_keys(Keys.ENTER)

            # Open dropdown
            category_btn.click()
            self.wait.until(EC.element_to_be_clickable(dropdown_options[0]))

            # Select correct category
            dropdown_options[test_case["category"]].click()

            # Close dropdown
            category_btn.click()
            self.wait.until(EC.invisibility_of_element(dropdown_options[0]))

            # Wait for stuff to get fetched
            time.sleep(1)

            # Wait until results get fetched
            self.wait.until(lambda d: len(search_left.find_elements(By.XPATH, "//div[@class='search-card-wrapper desktop-only']/child::div[@class='search-card-inner']//div[@class='search-card']")) > 0)

            # Check by card titles
            card_titles = [title.text.split("\n")[0] for title in search_left.find_elements(By.XPATH, "//div[@class='search-card-wrapper desktop-only']/child::div[@class='search-card-inner']//div[@class='search-card']")]
            self.assertTrue(len(card_titles) == 1 and card_titles[0] == word, f"Logic error when searching.{card_titles}")

            # Open dropdown
            category_btn.click()
            self.wait.until(EC.element_to_be_clickable(dropdown_options[0]))

            # Unselect correct category
            dropdown_options[test_case["category"]].click()

            # Close dropdown
            category_btn.click()
            self.wait.until(EC.invisibility_of_element(dropdown_options[0]))

    def test_05_logic_wrong_cases(self):
        """Test the functionality of Search when selected category is wrong."""

        # Test for 'search-left'
        search_left = self.driver.find_element(By.XPATH, "//div[@class='search-left']")
        self.assertTrue(search_left.is_displayed(), "Search left side should be visible")

        # Test for 'Kategoriya tanlang' button
        category_btn = search_left.find_element(By.XPATH, "//div[@class='sidebar-input-group']/child::div[@class='select-input']//div[@class='select-content']")
        self.assertTrue(category_btn.is_displayed(), "'Kategoriya tanlang' button should be visible")

        # Test for 'searchbox'
        searchbox = self.driver.find_element(By.XPATH, "//div[@class='search-left']//input[@id='search']")
        self.assertTrue(searchbox.is_displayed(), "Search box should be visible")

        # Wait for the dropdown to appear
        dropdown_options = category_btn.find_elements(By.XPATH, "//div[@class='sidebar-input-group']/child::div[@class='select-input']//div[@class='select-content']//div[@class='select-options ']//div[@class='option ']//div[@class='left']/child::div")

        for option in dropdown_options:
            self.assertFalse(option.is_displayed(), "Option should not be visible")

        # Open dropdown
        category_btn.click()
        self.wait.until(EC.element_to_be_clickable(dropdown_options[0]))

        for option in dropdown_options:
            self.assertTrue(option.is_displayed(), "Option should be visible")

        test_cases = [
            {
                "category": 0,
                "name": 'Forward Academy',
            },
            {
                "category": 2,
                "name": '"Everest" o\'quv markazi, Parkentskiy filiali',
            },
            {
                "category": 4,
                "name": 'Python Teacher',
            }
        ]

        # Select everything
        for i in range(5):
            dropdown_options[i].click()
            time.sleep(0.2)

        # Close dropdown
        category_btn.click()
        self.wait.until(EC.invisibility_of_element(dropdown_options[0]))

        for test_case in test_cases:

            # Type into searchbox
            word = test_case["name"]

            searchbox.clear()
            searchbox.send_keys(word)
            searchbox.send_keys(Keys.ENTER)

            # Open dropdown
            category_btn.click()
            self.wait.until(EC.element_to_be_clickable(dropdown_options[0]))

            # Unselect correct category
            dropdown_options[test_case["category"]].click()

            # Close dropdown
            category_btn.click()
            self.wait.until(EC.invisibility_of_element(dropdown_options[0]))

            # Wait for stuff to get fetched
            time.sleep(3)

            # Check by card titles
            card_titles = [title.text.split("\n")[0] for title in search_left.find_elements(By.XPATH, "//div[@class='search-card-wrapper desktop-only']/child::div[@class='search-card-inner']//div[@class='search-card']")]
            self.assertTrue(len(card_titles) == 0, "Found card from wrong category")

            # Open dropdown
            category_btn.click()
            self.wait.until(EC.element_to_be_clickable(dropdown_options[0]))

            # Select correct category
            dropdown_options[test_case["category"]].click()

            # Close dropdown
            category_btn.click()
            self.wait.until(EC.invisibility_of_element(dropdown_options[0]))

        # Open dropdown
        category_btn.click()
        self.wait.until(EC.element_to_be_clickable(dropdown_options[0]))

        # Unselect everything
        for i in range(5):
            dropdown_options[i].click()
            time.sleep(0.2)

        # Close dropdown
        category_btn.click()
        self.wait.until(EC.invisibility_of_element(dropdown_options[0]))

    def test_06_logic_all_cases(self):
        """Test the functionality of Search when selected all categories."""

        # Test for 'search-left'
        search_left = self.driver.find_element(By.XPATH, "//div[@class='search-left']")
        self.assertTrue(search_left.is_displayed(), "Search left side should be visible")

        # Test for 'Kategoriya tanlang' button
        category_btn = search_left.find_element(By.XPATH, "//div[@class='sidebar-input-group']/child::div[@class='select-input']//div[@class='select-content']")
        self.assertTrue(category_btn.is_displayed(), "'Kategoriya tanlang' button should be visible")

        # Test for 'searchbox'
        searchbox = self.driver.find_element(By.XPATH, "//div[@class='search-left']//input[@id='search']")
        self.assertTrue(searchbox.is_displayed(), "Search box should be visible")

        # Wait for the dropdown to appear
        dropdown_options = category_btn.find_elements(By.XPATH, "//div[@class='sidebar-input-group']/child::div[@class='select-input']//div[@class='select-content']//div[@class='select-options ']//div[@class='option ']//div[@class='left']/child::div")

        for option in dropdown_options:
            self.assertFalse(option.is_displayed(), "Option should not be visible")

        # Open dropdown
        category_btn.click()
        self.wait.until(EC.element_to_be_clickable(dropdown_options[0]))

        for option in dropdown_options:
            self.assertTrue(option.is_displayed(), "Option should be visible")

        test_cases = [
            {
                "category": 0,
                "name": 'Forward Academy',
            },
            {
                "category": 2,
                "name": '"Everest" o\'quv markazi, Parkentskiy filiali',
            },
            {
                "category": 4,
                "name": 'Python Teacher',
            }
        ]

        # Select everything
        for i in range(5):
            dropdown_options[i].click()
            time.sleep(0.2)

        # Close dropdown
        category_btn.click()
        self.wait.until(EC.invisibility_of_element(dropdown_options[0]))

        for test_case in test_cases:

            # Type into searchbox
            word = test_case["name"]

            searchbox.clear()
            searchbox.send_keys(word)
            searchbox.send_keys(Keys.ENTER)

            # Wait for stuff to get fetched
            time.sleep(1)

            # Wait until results get fetched
            self.wait.until(lambda d: len(search_left.find_elements(By.XPATH, "//div[@class='search-card-wrapper desktop-only']/child::div[@class='search-card-inner']//div[@class='search-card']"))>0)

            # Check by card titles
            card_titles = [title.text.split("\n")[0] for title in search_left.find_elements(By.XPATH, "//div[@class='search-card-wrapper desktop-only']/child::div[@class='search-card-inner']//div[@class='search-card']")]
            self.assertTrue(len(card_titles) == 1 and card_titles[0] == word, f"Logic error when searching.{card_titles}")

        # Open dropdown
        category_btn.click()
        self.wait.until(EC.element_to_be_clickable(dropdown_options[0]))

        # Unselect everything
        for i in range(5):
            dropdown_options[i].click()
            time.sleep(0.2)

        # Close dropdown
        category_btn.click()
        self.wait.until(EC.invisibility_of_element(dropdown_options[0]))