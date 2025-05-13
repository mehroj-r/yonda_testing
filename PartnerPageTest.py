from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from BasePageTest import BasePageTest


class PartnerPageTest(BasePageTest):

    PARTNER_URL = "https://yonda.uz/partner"
    active_navigation_idx = 1

    def test_01_text_content(self):
        """Test that the header content is correct."""
        header_div = self.driver.find_element(By.CLASS_NAME, "partnership-header")

        title = header_div.find_element(By.CSS_SELECTOR, ".p-left-side .title").text
        description = header_div.find_element(By.CSS_SELECTOR, ".p-left-side .description").text
        contact_title = header_div.find_element(By.CSS_SELECTOR, ".partner-contact-card .title").text

        self.assertEqual(title, "Yonda hamkoriga aylaning", "Text mismatch")
        self.assertEqual(description, "Ilovamiz orqali markazingizni ommalashtiring va mijozlar oqimini oshiring.", "Text mismatch")
        self.assertIn("Maxsus taklifga ega bo'lish uchun kontaktingizni qoldiring.", contact_title, "Text mismatch")

    def test_02_form_submission(self):
        """Test that the form submission is correct."""

        # Locate 'partner-contact-card'
        partner_card = self.driver.find_element(By.CLASS_NAME, "partner-contact-card")

        phone_input = partner_card.find_element(By.CSS_SELECTOR, 'input[type="tel"]')
        submit_button = partner_card.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

        # Type dummy phone number
        phone_input.clear()
        phone_input.send_keys(" 90 123 45 67")

        # Click submit button
        self.wait.until(EC.element_to_be_clickable(submit_button))
        self.driver.execute_script("arguments[0].click();", submit_button)

        # Check if value is the number we entered
        self.assertEqual(phone_input.get_attribute("value"), "+998 90 123 45 67", "Phone number should be inputted properly")

        # Wait for modal to appear
        modal = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".success-modal-overlay")))

        # Check modal content
        title = modal.find_element(By.CSS_SELECTOR, ".success-modal-title").text
        subtitle = modal.find_element(By.CSS_SELECTOR, ".success-modal-subtitle").text

        # Checck contents
        self.assertEqual(title, "Arizangiz qabul qilindi!", "Text mismatch")
        self.assertEqual(subtitle, "Tez orada siz bilan bog'lanamiz", "Text mismatch")

        # Close the modal
        close_button = modal.find_element(By.CSS_SELECTOR, ".success-modal-close")
        close_button.click()

        # Wait until modal disappears
        self.wait.until(EC.invisibility_of_element_located(modal))

    def test_03_statistics_cards(self):
        """Test that the statistics cards are correct."""
        stats_cards = self.driver.find_elements(By.CLASS_NAME, "statistics-card")
        self.assertEqual(len(stats_cards), 3)

        expected_titles = [
            "Yuklab olishlar soni",
            "Markazlar tanlovi",
            "Hamkorlar ishonchi"
        ]

        for i, card in enumerate(stats_cards):
            title = card.find_element(By.CLASS_NAME, "title").text
            number = card.find_element(By.CLASS_NAME, "number").text

            # Check the title is expected
            self.assertEqual(title, expected_titles[i], "Title should be present in the card.")

            # Check number is in the correct format (e.g., digits followed by "+")
            self.assertRegex(number, r"^\d+\+$", "Number should be present in the card.")

    def test_04_partners_benefits_cards(self):
        """Test that the partners benefits cards are correct."""
        card_titles = [card.text for card in self.driver.find_elements(By.CSS_SELECTOR, ".partners-container .partners-card")]
        self.assertEqual(len(card_titles), 3)

        expected_titles = [
            "Yangi mijozlar",
            "Barqaror foyda",
            "Promo-takliflar"
        ]

        self.assertEqual(sorted(card_titles), sorted(expected_titles), "Card titles should be correct.")

    def test_05_progress_steps(self):
        """Test that the progress steps are correct."""
        steps_titles = [step.text for step in self.driver.find_elements(By.XPATH, "//div[@class='partners-row']//div[@class='progress-card']//p[@class='card-title']")]
        self.assertGreaterEqual(len(steps_titles), 4)

        expected_step_phrases = [
            "Maxsus taklif uchun ariza qoldirasiz",
            "Menejerimizdan konsultatsiya olasiz",
            "Darslar jadvali va kerakli ma’lumotlarni kiritasiz",
            "Ilova orqali yangi mijozlar oqimini kutib olasiz!"
        ]

        self.assertEqual(sorted(steps_titles), sorted(expected_step_phrases), "Step titles should be correct.")

    def test_06_benefit_section_content(self):
        """Test that the benefit section content is correct."""

        # Locate 'benefit'
        benefit_div = self.driver.find_element(By.CSS_SELECTOR, ".benefit")

        # Check section title
        benefit_title = "Yonda sizga qanday foyda keltiradi?"
        section_title = benefit_div.find_element(By.CSS_SELECTOR, ".benefit .title").text
        self.assertEqual(section_title, benefit_title, "Section title should be correct.")

        # Check benefit cards
        cards = benefit_div.find_elements(By.CSS_SELECTOR, ".benefit-card")
        self.assertEqual(len(cards), 6)

        expected_titles = [
            {
                "title":"Ko’proq mijozlar",
                "description": "O’quv markazingiz ilovaga kiritilgach, xizmatlaringiz ommalashishni boshlaydi va diskaveri-karta orqali mijozlar oqimi ko’payadi."
            },
            {
                "title": "Shaffof analitika",
                "description": "Ilova sizga mijozlaringiz va ularning qatnovini uzluksiz kuzatish, sotuv jarayonlarini tahlil qilish va foydalanuvchilarning fikri bilan tanishib borish imkonini beradi."
            },
            {
                "title": "Ko’proq daromad",
                "description": "Yonda foydalanuvchilari sizning potensial mijozlaringizga aylanadi, to’lovdagi qulayliklar esa ularni xizmatlaringizdan doimiy foydalanishga undaydi."
            },
            {
                "title": "Oilaviy auditoriya",
                "description": "Parent’s Child tizimi o’quvchilardan tashqari ularning ota-onalari bilan ham samarali aloqa o’rnatish va sodiqlik dasturlarini ishlab chiqishingizga yordam beradi."
            },
            {
                "title": "Qulay tizim",
                "description": "Ilova orqali yangi mashg’ulotlar va kurslarni kiritish, dars jadvallarini joylashtirish va yangilash imkoni mavjud."
            },
            {
                "title": "Konsultatsiya va mentoring",
                "description": "Yakka tartibda ishlovchi ekspertlar va repetitorlar ham o’z xizmatlarini targ’ib qilishlari, individual mashg’ulot va konsultatsiyalar tashkil etishlari mumkin bo’ladi."
            }

        ]

        for i, card in enumerate(cards):
            title = card.find_element(By.CLASS_NAME, "card-title").text
            description = card.find_element(By.CLASS_NAME, "card-description").text
            self.assertEqual(title, expected_titles[i]["title"], "Title should be correct.")
            self.assertEqual(description, expected_titles[i]["description"], "Description should be correct.")

    def test_07_more_info_content_and_form(self):
        """Test that the more information content is correct."""

        # Check main card
        card = self.driver.find_element(By.CLASS_NAME, "more-information-card")

        # Check title text
        actual_title_desktop = card.find_element(By.XPATH, "//div[@class='title']//span[@class='desktop-text']").text
        expected_title_desktop = "To'liq ma'lumot olish uchun kontaktingizni qoldiring"
        self.assertEqual(expected_title_desktop, actual_title_desktop)

        # Check dscription text
        actual_desc_desktop = card.find_element(By.XPATH, "//div[@class='description']//span[@class='desktop-text']").text
        expected_desc_desktop = "Menejerimiz siz bilan bog'lanishi uchun"
        self.assertEqual(expected_desc_desktop, actual_desc_desktop)

        # Check form input
        phone_input = card.find_element(By.CSS_SELECTOR, "form input[type='tel']")
        self.assertTrue(phone_input.get_attribute("placeholder").startswith("+998 "))

        # Check submit button
        submit_button = card.find_element(By.CSS_SELECTOR, "form button[type='submit']")
        self.assertEqual(submit_button.text.strip(), "Yuborish")

        # Type dummy phone number
        phone_input.clear()
        phone_input.send_keys(" 90 123 45 67")

        # Click submit button
        self.wait.until(EC.element_to_be_clickable(submit_button))
        self.driver.execute_script("arguments[0].click();", submit_button)

        # Check if value is the number we entered
        self.assertEqual(phone_input.get_attribute("value"), "+998 90 123 45 67",
                         "Phone number should be inputted properly")

        # Wait for modal to appear
        modal = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".success-modal-overlay")))

        # Check modal content
        title = modal.find_element(By.CSS_SELECTOR, ".success-modal-title").text
        subtitle = modal.find_element(By.CSS_SELECTOR, ".success-modal-subtitle").text

        # Checck contents
        self.assertEqual(title, "Arizangiz qabul qilindi!", "Text mismatch")
        self.assertEqual(subtitle, "Tez orada siz bilan bog'lanamiz", "Text mismatch")

        # Close the modal
        close_button = modal.find_element(By.CSS_SELECTOR, ".success-modal-close")
        close_button.click()

        # Wait until modal disappears
        self.wait.until(EC.invisibility_of_element_located(modal))
