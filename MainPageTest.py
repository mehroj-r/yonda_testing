import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from BasePageTest import BasePageTest


class MainPageTest(BasePageTest):

    def test_01_latest_search_section(self):
        """Test the content of the latest search section. """

        # Locate 'latest-search'
        latest_search = self.driver.find_element(By.CLASS_NAME, "latest-search")

        # Test for 'Songgi qidiruvlar' text
        songgi_qidiruvlar_text = latest_search.find_element(By.XPATH,"//div[@class='title' and contains(text(), 'So‘nggi qidiruvlar')]")
        self.assertTrue(songgi_qidiruvlar_text.is_displayed(), "So'nggi qidiruvlar title should be visible")

        # Test for 'latest-search-card' to be at least 1
        latest_search_cards = latest_search.find_elements(By.CLASS_NAME, "latest-search-card")
        self.assertGreater(len(latest_search_cards), 0, "At least one latest search card should be present")

        # Test for 'Ko'proq ko'rish' button
        koproq_korish_button = latest_search.find_element(By.XPATH, "//button[@class='more']//span[contains(text(), \"Ko'proq ko'rish\")]")
        self.assertTrue(koproq_korish_button.is_displayed(), "'Ko'proq ko'rish' button should be visible")

        # Wait for the button to be clickable
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='more']//span[contains(text(), \"Ko'proq ko'rish\")]"))
        )

        # Scroll into view to prevent interception
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)

        # Click it when becomes clickable
        self.wait.until(EC.element_to_be_clickable(button))
        self.driver.execute_script("arguments[0].click();", button)

        # Wait for new cards to load
        self.wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "latest-search-card")) != len(latest_search_cards))

        # Apply assertions
        new_search_cards = self.driver.find_elements(By.CLASS_NAME, "latest-search-card")
        self.assertGreater(len(new_search_cards), len(latest_search_cards), "Click more should load more cards")

    def test_02_category_section(self):
        """Test the content of the category section."""

        # Locate 'category'
        category = self.driver.find_element(By.CLASS_NAME, "category")

        # Test for 'Kategoriya' title
        kategoriya_text = category.find_element(By.XPATH, "//div[@class='title' and contains(text(), 'Kategoriya')]")
        self.assertTrue(kategoriya_text.is_displayed(), "'Kategoriya' title should be visible")

        # Test for  5 category cards exist
        category_cards = category.find_elements(By.CLASS_NAME, "category-card")
        self.assertEqual(len(category_cards), 5, "There should be 5 category cards")

        # Expected card titles (in order)
        expected_titles = ["Sport", "Ta’lim", "IT", "San’at", "Repetitor"]
        actual_titles = list(title.text for title in category.find_elements(By.XPATH, "//div[@class='category-card']/descendant::div[@class='card-title']"))

        # Test faq titles
        self.assertEqual(sorted(expected_titles), sorted(actual_titles), "Faq titles should be the same")

        # Test 'Ilova yuklab olish' link
        ilova_yuklab_olish_link = category.find_element(By.XPATH,"//p[@class='w-full']//a[contains(text(), 'Ilova yuklab olish')]")
        self.assertTrue(ilova_yuklab_olish_link.is_displayed(), "'Ilova yuklab olish' link should be visible")

    def test_03_benefits_section(self):
        """Test the content of the benefits section. """

        # Locate 'properties'
        properties = self.driver.find_element(By.CLASS_NAME, "properties")

        # Test for 'Afzalliklari' text
        afzalliklari_text = properties.find_element(By.XPATH,"//div[@class='title' and contains(text(), 'Afzalliklari')]")
        self.assertTrue(afzalliklari_text.is_displayed(), "Afzalliklari title should be visible")

        # Test for 'property_card' to be 4
        property_card_button = properties.find_elements(By.CLASS_NAME, "property-card")
        self.assertEqual(len(property_card_button), 4, "There should be 4 property cards")

    def test_04_promotion_section(self):
        """Test the content of the promotion section. """

        # Locate 'all-yonda'
        all_yonda = self.driver.find_element(By.CLASS_NAME, "all-yonda")

        # Test for 'Endi hammasi Yonda!' text
        endi_hammasi_yonda_text = all_yonda.find_element(By.XPATH,"//div[@class='title' and contains(text(), 'Endi hammasi Yonda!')]")
        self.assertTrue(endi_hammasi_yonda_text.is_displayed(), "Endi hammasi Yonda! title should be visible")

        # Test for 'Imkoniyatlaringiz xaritasini oching' text
        imkoniyatlaringiz_xaritasi_text = all_yonda.find_element(By.XPATH,"//div[@class='description' and contains(text(), 'Imkoniyatlaringiz xaritasini oching')]")
        self.assertTrue(imkoniyatlaringiz_xaritasi_text.is_displayed(), "Imkoniyatlaringiz xaritasini oching description should be visible")

        # Expected values for 'all-yonda-card's
        expected_cards = [
            {
                "title": "Yonda‘ni yuklab oling",
                "description": "Shunchaki tugmani bosing va ilova sizda!",
            },
            {
                "title": "Yo’nalishlar bilan tanishing",
                "description": "Kerakli markazlarni osongina toping",
            },
            {
                "title": "Rivojlanishni boshlang",
                "description": "Qiyoslang, tanlang va harakatni boshlang!",
            }
        ]

        # Find the cards
        all_yonda_cards = all_yonda.find_elements(By.CLASS_NAME, "all-yonda-card")
        self.assertEqual(len(all_yonda_cards), len(expected_cards), "Number of cards should match expected count")

        # Test card titles
        expected_title = ["Yonda‘ni yuklab oling", "Yo’nalishlar bilan tanishing", "Rivojlanishni boshlang"]
        actual_titles = [title.text for title in all_yonda.find_elements(By.XPATH, "//div[@class='card-title normal' or @class='card-title unnormal']")]
        self.assertEqual(sorted(expected_title), sorted(actual_titles), "Faq titles should be the same")

        # Test card descriptions
        expected_descs = ["Shunchaki tugmani bosing va ilova sizda!", "Kerakli markazlarni osongina toping", "Qiyoslang, tanlang va harakatni boshlang!"]
        actual_descs = [desc.text for desc in all_yonda.find_elements(By.XPATH,"//div[@class='card-description normal' or @class='card-description unnormal']")]
        self.assertEqual(sorted(expected_descs), sorted(actual_descs), "Faq desciptions should be the same")

    def test_05_app_downloads_section(self):
        """Test the content of the app downloads section. """

        # Locate the download-app-card
        download_card = self.driver.find_element(By.CLASS_NAME, "download-app-card")

        # Test the title
        title_elem = download_card.find_element(By.CSS_SELECTOR, ".title h2")
        expected_title = "Yonda bilan rivojlanish qulay va samarali"
        self.assertEqual(
            title_elem.get_attribute("innerText").replace("\n", " ").strip(),
            expected_title,
            f"Main title should be '{expected_title}'"
        )

        # Test the paragraph text
        paragraph_elem = download_card.find_element(By.CSS_SELECTOR, ".title p")
        expected_paragraph = "Ilovani yuklab oling va bugunoq maqsadlarga qadam tashlang!"
        self.assertEqual(
            paragraph_elem.get_attribute("innerText").replace("\n", " ").strip(),
            expected_paragraph,
            f"Paragraph text should be '{expected_paragraph}'"
        )

        # Test the image element
        img_elem = download_card.find_element(By.CSS_SELECTOR, ".image img")
        src = img_elem.get_attribute("src")
        self.assertTrue(src and "dwonload-app-card" in src, "Image src should contain 'dwonload-app-card'")

        # Test there are exactly 2 download buttons
        download_buttons = download_card.find_elements(By.CLASS_NAME, "download-button")
        self.assertEqual(len(download_buttons), 2, "There should be exactly 2 download buttons")

        # Test platform logos
        expected_logos = ["google-play-logo.svg", "apple-logo.svg"]
        actual_logos = [logo.get_attribute("src").split("/")[-1] for logo in download_card.find_elements(By.CSS_SELECTOR, ".logo img")]
        self.assertEqual(sorted(expected_logos), sorted(actual_logos), "Faq logos should be the same")