import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from TestUtils import TestUtils


class BasePageTest(unittest.TestCase):
    """Base test class with common functionality for all page tests."""

    BASE_URL = "https://yonda.uz"
    SEARCH_URL = None
    PARTNER_URL = None
    REGISTER_BUSINESS_URL = None
    REGISTER_REPETITOR_URL = None
    EXECUTABLE_PATH = "./chromedriver"
    active_navigation_idx = None
    skip_footer = False

    @classmethod
    def setUpClass(cls):
        """Set up the test environment once before all test methods."""
        if cls.SEARCH_URL:
            cls.driver = TestUtils.setup_browser(cls.SEARCH_URL, cls.EXECUTABLE_PATH)
        elif cls.PARTNER_URL:
            cls.driver = TestUtils.setup_browser(cls.PARTNER_URL, cls.EXECUTABLE_PATH)
        elif cls.REGISTER_BUSINESS_URL:
            cls.driver = TestUtils.setup_browser(cls.REGISTER_BUSINESS_URL, cls.EXECUTABLE_PATH)
        elif cls.REGISTER_REPETITOR_URL:
            cls.driver = TestUtils.setup_browser(cls.REGISTER_REPETITOR_URL, cls.EXECUTABLE_PATH)
        else:
            cls.driver = TestUtils.setup_browser(cls.BASE_URL, cls.EXECUTABLE_PATH)
        cls.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests have run."""
        cls.driver.quit()

    def clickLinkTest(self, target_element, target_link, exact_match=True):
        """Tests if clicking passed element redirects to that link in the same tab"""
        result = TestUtils.click_link_test(self.driver, self.wait, target_element, target_link, exact_match)
        self.assertTrue(result, f"Link did not redirect to expected URL: {target_link}")

    def clickExternalLinkTest(self, target_element, target_link, exact_match=True):
        """Tests if clicking passed element opens the correct link in a new tab"""
        result = TestUtils.click_external_link_test(self.driver, self.wait, target_element, target_link, exact_match)
        self.assertTrue(result, f"External link did not open expected URL: {target_link}")

    def extract_text_without_propagation(self, tag):
        return TestUtils.extract_text_without_propagation(self.driver, tag)

    def test_001_page_title(self):
        """Test that the page title is correct."""
        self.assertIn("Yonda", self.driver.title, "Page title should contain 'Yonda'")

    def test_002_header_navigation_left_side(self):
        """Test that the main navigation links are present."""
        links_div = self.driver.find_element(By.XPATH, "//div[@class='container']/child::div[@class='left-side']//div[@class='links ']")

        links = links_div.find_elements(By.CLASS_NAME, "link")
        self.assertEqual(len(links), 2, "Navigation links should contain 2 links")

        expected_values = [
            {
                "text": "Izlash",
                "href": f"{self.BASE_URL}/search",
            },
            {
                "text": "Hamkorlik",
                "href": f"{self.BASE_URL}/partner",
            }
        ]

        for i, link in enumerate(links[:2]):
            self.assertEqual(link.text, expected_values[i]["text"], "Link text should be the same")
            self.assertEqual(link.get_attribute("href"), expected_values[i]["href"], "Link href should be the same")

            # Don't click the active link on the active page
            if not (self.active_navigation_idx == i):
                self.clickLinkTest(link, expected_values[i]["href"])

    def test_003_header_navigation_right_side(self):
        """Test that the right side navigation elements are present."""
        # == Right side ==
        right_side = self.driver.find_element(By.XPATH, "//div[@class='container']/child::div[@class='right-side']")

        # Test for arrow dropdown
        arrow_dropdown = right_side.find_element(By.XPATH, "//img[@src='/icons/arrow-down.svg' and @alt='open-select']")
        self.assertTrue(arrow_dropdown.is_displayed(), "Arrow dropdown icon should be visible")

        # Test for 'Ilova yuklab olish' link
        ilova_yuklab_olish_link = right_side.find_element(By.LINK_TEXT, "Ilova yuklab olish")
        self.assertTrue(ilova_yuklab_olish_link.is_displayed(), "Ilova yuklab olish link should be visible")

        # Test for 'Ro'yxatdan o'tish' link

        # Skip it if /partner page is active
        if self.active_navigation_idx == 2:
            return

        royxatdan_otish_link = right_side.find_element(By.LINK_TEXT, "Ro\'yxatdan o'tish")
        self.assertTrue(royxatdan_otish_link.is_displayed(), "Ro'yxatdan o'tish link should be visible")
        self.clickLinkTest(royxatdan_otish_link, self.BASE_URL + "/register")

    def test_004_header_navigation_faq_dropdown(self):
        """Test that the FAQ dropdown works correctly."""
        # == Left side ==
        left_side = self.driver.find_element(By.XPATH, "//div[@class='container']/child::div[@class='left-side']")

        # Test for 'Savollar va javoblar' dropdown
        savollar_dropdown = left_side.find_element(By.XPATH, "//span[contains(text(), 'Savollar va javoblar')]")
        self.assertTrue(savollar_dropdown.is_displayed(), "Savollar va javoblar dropdown should be visible")

        # Expected options for dropdown
        expected_options = [
            {
                "text": "Hamkorlar uchun",
                "href": f"{self.BASE_URL}/faq-partners",
            },
            {
                "text": "Foydalanuvchilar uchun",
                "href": f"{self.BASE_URL}/faq-users",
            }
        ]

        #  Test for faq select options of dropdown (before and after clicking)
        faq_options = left_side.find_elements(By.CLASS_NAME, "option")
        self.assertEqual(len(expected_options), len(faq_options), "Faq options count should be the same.")

        for option in faq_options:
            self.assertFalse(option.is_displayed(), "Faq option should not be visible")

        # Test for validity of options
        for i, option in enumerate(faq_options[:2]):
            # Scroll into the element to avoid interception
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", savollar_dropdown)

            # Click dropdown
            self.wait.until(EC.element_to_be_clickable(savollar_dropdown))
            self.driver.execute_script("arguments[0].click();", savollar_dropdown)

            # Wait for the option to be clickable
            self.wait.until(EC.element_to_be_clickable(option))

            # Apply tests
            self.assertTrue(option.is_displayed(), "Faq option should be visible")
            self.assertEqual(option.text, expected_options[i]["text"], "Faq option text is mismatched.")
            self.assertEqual(option.get_attribute("href"), expected_options[i]["href"],
                             "Faq option href link is mismatched.")
            self.clickLinkTest(option, expected_options[i]["href"])

    def test_005_footer_section(self):
        """Tests the contents of the footer section."""

        if self.skip_footer:
            return

        # Locate the footer
        footer = self.driver.find_element(By.TAG_NAME, "footer")

        # Top Part: Logo
        logo_img = footer.find_element(By.CSS_SELECTOR, ".top-part .logo img")
        self.assertEqual(logo_img.get_attribute("alt"), "Yonda logo", "Footer logo alt text should be 'Yonda logo'")
        self.assertTrue("/images/logo.svg" in logo_img.get_attribute("src"),
                        "Footer logo src should contain '/images/logo.svg'")

        # Middle Part: Columns
        columns = footer.find_elements(By.CSS_SELECTOR, ".middle-part .column")
        self.assertEqual(len(columns), 4, "Footer should have 4 columns")

        # FAQ Links
        faq_column = columns[0]
        faq_title = faq_column.find_element(By.CLASS_NAME, "title").text.strip()
        self.assertEqual(faq_title, "Savollar va javoblar", "First column title should be 'Savollar va javoblar'")

        faq_links = faq_column.find_elements(By.CSS_SELECTOR, ".content .content-item")
        self.assertEqual(faq_links[0].text.strip(), "Hamkorlar uchun", "First FAQ link should be 'Hamkorlar uchun'")
        self.assertEqual(faq_links[0].get_attribute("href").split("/")[-1], "faq-partners",
                         "First FAQ link should point to 'faq-partners'")

        self.assertEqual(faq_links[1].text.strip(), "Foydalanuvchilar uchun",
                         "Second FAQ link should be 'Foydalanuvchilar uchun'")
        self.assertEqual(faq_links[1].get_attribute("href").split("/")[-1], "faq-users",
                         "Second FAQ link should point to 'faq-users'")

        # Column 2: Documents
        docs_column = columns[1]
        docs_title = docs_column.find_element(By.CLASS_NAME, "title").text.strip()
        self.assertEqual(docs_title, "Hujjatlar", "Second column title should be 'Hujjatlar'")

        docs_links = docs_column.find_elements(By.CSS_SELECTOR, ".content .content-item")
        self.assertIn("privacy-policy", docs_links[0].get_attribute("href"),
                      "First document link should contain 'privacy-policy'")
        self.assertIn("Ommaviy oferta", docs_links[1].text, "Second document link should contain 'Ommaviy oferta'")

        # Column 3: Contact Info
        contact_column = columns[2]
        contact_title = contact_column.find_element(By.CLASS_NAME, "title").text.strip()
        self.assertEqual(contact_title, "Kontaktlar", "Third column title should be 'Kontaktlar'")

        contact_info = contact_column.find_element(By.CLASS_NAME, "content-item").text
        self.assertIn("Toshkent shahri", contact_info, "Contact info should contain 'Toshkent shahri'")

        # Column 4: App Download Buttons
        download_buttons = columns[3].find_elements(By.CLASS_NAME, "download-button")
        self.assertEqual(len(download_buttons), 2, "There should be 2 download buttons in the footer")

        # App links
        expected_links = [
            "https://play.google.com/store/apps/details?id=com.fivets.mobileapp",
            "https://apps.apple.com/uz/app/yonda-uz/id6642665299"
        ]

        for i, button in enumerate(download_buttons):
            href = button.get_attribute("href")
            self.assertTrue(href.startswith(expected_links[i]),
                            f"Download button {i} should link to {expected_links[i]}")
            self.clickExternalLinkTest(button, expected_links[i], False)

        # Bottom Part: Copyright
        copyright_text = footer.find_element(By.CSS_SELECTOR, ".bottom-part").text
        self.assertIn("©Yonda", copyright_text, "Copyright should contain '©Yonda'")
        self.assertIn("2025", copyright_text, "Copyright should contain the year '2025'")