import random, time, os

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from BasePageTest import BasePageTest


class RegisterBusinessPageTest(BasePageTest):

    REGISTER_BUSINESS_URL = "https://yonda.uz/register"
    active_navigation_idx = 2

    def test_01_form_required_fields(self):
        """ Test that the required fields are present. """

        # Check the title
        title = self.driver.find_element(By.TAG_NAME, "h1").text
        self.assertEqual(title, "Yonda ilovasida biznes akkauntini olish uchun quyidagi formani to‘ldiring:")

        # Locate the div
        form_div = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]")

        # Extract labels
        actual_labels = map(lambda label: self.extract_text_without_propagation(label), form_div.find_elements(By.TAG_NAME, "label"))

        # Check for all labels
        expected_labels = [
            "Biznes nomi", "Biznes kategoriyasi", "Tel raqami", "Elektron pochta", "Biznes ish vaqtlari"
        ]

        # Verify that labels match
        self.assertEqual(sorted(actual_labels), sorted(expected_labels), "Required fields are mismatched.")

    def test_02_form_empty_submission(self):
        """Test for empty submission."""

        # Click submit button
        submit_button = self.driver.find_element(By.XPATH, "//button[.//span[text()='Davom etish']]")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        self.wait.until(EC.element_to_be_clickable(submit_button))
        self.driver.execute_script("arguments[0].click();", submit_button)

        # Fields should still be empty and marked invalid
        name_input = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/form/div[1]/input")
        category_label = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/form/div[2]/label")
        phone_div = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/form/div[3]/div")
        email_input = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/form/div[4]/input")
        business_days_label = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/form/div[5]/label")

        # 'aria-invalid'/'data-error' should remain true
        self.assertEqual(name_input.get_attribute("aria-invalid"), "true")
        self.assertEqual(category_label.get_attribute("data-error"), "true")
        self.assertEqual(email_input.get_attribute("aria-invalid"), "true")
        self.assertEqual(phone_div.get_attribute("aria-invalid"), "true")
        self.assertEqual(business_days_label.get_attribute("data-error"), "true")

    def test_03_form_valid_submission(self):
        """ Test for valid submission. """

        # == FIll in business name ==
        name_input = self.driver.find_element(By.NAME, "name")
        name_input.clear()
        name_input.send_keys("My Test Biznes")

        # == Fill in business category ==
        category_dropdown = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/form/div[2]/button")

        # Open dropdown
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", category_dropdown)
        self.wait.until(EC.element_to_be_clickable(category_dropdown))
        self.driver.execute_script("arguments[0].click();", category_dropdown)

        dropdown_options = self.driver.find_elements(By.XPATH, "/html/body/div/div/div/div/div/div")

        # Expected categories
        self.wait.until(EC.element_to_be_clickable(dropdown_options[0]))
        expected_categories = ["IT", "Sport", "San’at", "Ta’lim"]
        actual_categories = [option.text for option in dropdown_options]
        self.assertEqual(sorted(expected_categories), sorted(actual_categories), "Categories should be the same")

        # Choose random option
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", category_dropdown)
        self.wait.until(EC.element_to_be_clickable(dropdown_options[0]))
        self.driver.execute_script("arguments[0].click();", dropdown_options[random.randint(0,3)])

        # == Fill in phone input ==
        phone_input = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, '99 999')]")
        phone_input.clear()
        phone_input.send_keys("90 123 45 67")

        # == Email fill in ==
        email_input = self.driver.find_element(By.NAME, "email")
        email_input.clear()
        email_input.send_keys(f"test_{random.randint(100,1000)}@email.com")

        # == FIll in business times ==
        random_days = random.sample(range(0,7), 3)

        # Locate day checkboxes
        day_chekboxes = self.driver.find_elements(By.XPATH, "/html/body/main/div/main/div/div[2]/form/div[5]/div/div/div[1]/button")

        for day in random_days:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", day_chekboxes[day])
            self.wait.until(EC.element_to_be_clickable(day_chekboxes[day]))
            self.driver.execute_script("arguments[0].click();", day_chekboxes[day])

        time.sleep(0.5)

        for day in random_days:
            for i in range(2):
                # Click dropdown
                target_dropdown = self.driver.find_element(By.XPATH, f"/html/body/main/div/main/div/div[2]/form/div[5]/div/div[{day+1}]/div[2]/button[{i+1}]")
                self.wait.until(EC.element_to_be_clickable(target_dropdown)).click()

                # Retrieve all options
                hour_options = self.driver.find_elements(By.XPATH, "/html/body/div/div/div[1]/div[1]/div")
                minute_options = self.driver.find_elements(By.XPATH, "/html/body/div/div/div[1]/div[2]/div")

                # Choose random option [HOUR]
                self.wait.until(EC.element_to_be_clickable(hour_options[i+10]))
                self.driver.execute_script("arguments[0].click();", hour_options[i+10])

                # Choose random option [MINUTE]
                self.wait.until(EC.element_to_be_clickable(minute_options[i+5]))
                self.driver.execute_script("arguments[0].click();", minute_options[i+5])

                # Close time dropdown
                target_dropdown.send_keys(Keys.ESCAPE)

        # Try submitting again
        submit_button = self.driver.find_element(By.XPATH, "//button[.//span[text()='Davom etish']]")
        self.wait.until(EC.element_to_be_clickable(submit_button))
        self.driver.execute_script("arguments[0].click();", submit_button)

    def test_04_address_required_fields(self):
        """ Test for address field present """

        # Check the title
        title = self.driver.find_element(By.TAG_NAME, "h1").text
        self.assertEqual(title, "Yonda ilovasida biznes akkauntini olish uchun quyidagi formani to‘ldiring:")

        # Locate the div
        address_div = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]")

        # Extract labels
        actual_labels = map(lambda label: self.extract_text_without_propagation(label), address_div.find_elements(By.TAG_NAME, "label"))

        # Check for all labels
        expected_labels = ["Manzil"]

        # Verify that labels match
        self.assertEqual(sorted(actual_labels), sorted(expected_labels), "Required fields are mismatched.")

    def test_05_address_empty_submission(self):
        """ Test for empty address field submission. """

        # Click submit button
        submit_button = self.driver.find_element(By.XPATH, "//button[.//span[text()='Davom etish']]")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        self.wait.until(EC.element_to_be_clickable(submit_button))
        self.driver.execute_script("arguments[0].click();", submit_button)

        # 'Manzilni kiritish shart' should be visible
        address_required_field = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/div[1]/div[1]/span")
        self.assertEqual(address_required_field.text, "Manzilni kiritish shart")

    def test_06_address_valid_submission(self):
        """ Test for valid address field submission. """

        # Fill in address field
        address_input = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/div[1]/div[1]/input")
        address_input.clear()
        address_input.send_keys("Chotqol koʻchasi, 7, Toshkent, Oʻzbekiston")

        time.sleep(3)

        # Choose the first suggestion
        search_options = self.driver.find_elements(By.XPATH, "/html/body/main/div/main/div/div[2]/div[1]/div[2]/div")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_options[0])
        self.wait.until(EC.element_to_be_clickable(search_options[0]))
        self.driver.execute_script("arguments[0].click();", search_options[0])

        time.sleep(1)

        # Click submit button
        submit_button = self.driver.find_element(By.XPATH, "//button[.//span[text()='Davom etish']]")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        self.wait.until(EC.element_to_be_clickable(submit_button))
        self.driver.execute_script("arguments[0].click();", submit_button)

        time.sleep(1)

    def test_07_benefit_required_fields(self):
        """ Test for benefits field present """

        # Check the title
        title = self.driver.find_element(By.TAG_NAME, "h1").text
        self.assertEqual(title, "Yonda ilovasida biznes akkauntini olish uchun quyidagi formani to‘ldiring:")

        # Locate the div
        benefits_div = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]")

        # Extract labels
        actual_labels = map(lambda label: self.extract_text_without_propagation(label), benefits_div.find_elements(By.TAG_NAME, "label"))

        # Check for all labels
        expected_labels = ["Afzalliklar"]

        # Verify that labels match
        self.assertEqual(sorted(actual_labels), sorted(expected_labels), "Required fields are mismatched.")

    def test_08_benefit_empty_submission(self):
        """Test for empty submission."""

        # Click submit button
        submit_button = self.driver.find_element(By.XPATH, "//button[.//span[text()='Davom etish']]")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        self.wait.until(EC.element_to_be_clickable(submit_button))
        self.driver.execute_script("arguments[0].click();", submit_button)

        # Fields should still be empty and marked invalid
        benefits_dropdown = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/div[1]/div/div")

        # 'input-error' CSS selector
        self.assertIn("input-error", benefits_dropdown.get_attribute("class"))

    def test_09_benefit_valid_submission(self):
        """Test for valid submission."""

        # Click benefits dropdown
        benefits_dropdown = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/div[1]/div/div")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", benefits_dropdown)
        self.wait.until(EC.element_to_be_clickable(benefits_dropdown))
        self.driver.execute_script("arguments[0].click();", benefits_dropdown)

        # Choose 3 random benfits
        benefit_options = self.driver.find_elements(By.XPATH, "/html/body/main/div/main/div/div[2]/div[1]/div/div[2]/div[contains(concat(' ', normalize-space(@class), ' '), ' flex ')]")
        random_options = random.sample(benefit_options, 3)

        for option in random_options:
            self.driver.execute_script("arguments[0].click();", option)

        # Click submit button
        submit_button = self.driver.find_element(By.XPATH, "//button[.//span[text()='Davom etish']]")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        self.wait.until(EC.element_to_be_clickable(submit_button))
        self.driver.execute_script("arguments[0].click();", submit_button)

    def test_10_image_required_fields(self):
        """Test for required fields present."""

        # Check the title
        title = self.driver.find_element(By.TAG_NAME, "h1").text
        self.assertEqual(title, "Biznes rasmi")

        # Locate the 'input' div
        input_div = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div[1]/div")

        # Check input-instruction content
        instruction_text = input_div.find_element(By.TAG_NAME, "p").text
        self.assertEqual(instruction_text, "Rasm turi PNG yoki JPEG (5MB gacha)")

        # Check input-button text
        input_btn_text = input_div.find_element(By.TAG_NAME, "button").text
        self.assertEqual(input_btn_text, "Rasm yuklash")

    def test_11_image_empty_submission(self):
        """Test for empty submission."""

        # Click submit button
        submit_button = self.driver.find_element(By.XPATH, "//button[.//span[text()='Yuklash']]")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        self.wait.until(EC.element_to_be_clickable(submit_button))
        self.driver.execute_script("arguments[0].click();", submit_button)

        # 'Rasm kiritish majburiy' should be visible
        image_required_warning = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div[1]/div[1]/p")
        self.assertEqual(image_required_warning.text, "Rasm kiritish majburiy")

    def test_12_image_valid_submission(self):
        """Test for valid submission."""

        file_path = os.path.abspath("image.jpeg")

        upload_input = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div[1]/div[2]/input")
        upload_input.send_keys(file_path)

        # Check if the img is actually uploaded
        uploaded_img = self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div[2]/div[2]/div/div[1]/img")))
        self.assertEqual(uploaded_img.get_attribute("alt"), "Uploaded image", "Image should be uploaded")

        # Click submit button
        submit_button = self.driver.find_element(By.XPATH, "//button[.//span[text()='Yuklash']]")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        self.wait.until(EC.element_to_be_clickable(submit_button))
        self.driver.execute_script("arguments[0].click();", submit_button)

        #  Wait for modal to be visible
        modal = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@role='dialog' and @data-state='open']"))
        )

        # Validate title
        title = modal.find_element(By.XPATH, ".//h2[@data-slot='dialog-title']")
        self.assertEqual(title.text.strip(), "Arizangiz qabul qilindi")

        # Validate description
        description = modal.find_element(By.XPATH, ".//p[@data-slot='dialog-description']")
        self.assertEqual(description.text.strip(), "Tez orada siz bilan aloqaga chiqamiz")

        # Validate success button
        success_button = modal.find_element(By.XPATH, ".//button[contains(text(), \"Bosh sahifaga o'tish\")]")
        self.assertTrue(success_button.is_displayed())