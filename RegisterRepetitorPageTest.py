import random, time, os
from datetime import datetime

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from BasePageTest import BasePageTest


class RegisterRepetitorPageTest(BasePageTest):
    REGISTER_REPETITOR_URL = "https://yonda.uz/register/repetitor"
    active_navigation_idx = 2

    def test_01_form_required_fields(self):
        """ Test that the required fields are present. """

        # Check the title
        title = self.driver.find_element(By.TAG_NAME, "h1").text
        self.assertEqual(title, "Yonda ilovasida repetitor akkauntini olish uchun quyidagi formani to‘ldiring:")

        # Locate the div
        form_div = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]")

        # Extract labels
        actual_labels = map(lambda label: self.extract_text_without_propagation(label),
                            form_div.find_elements(By.TAG_NAME, "label"))

        # Check for all labels
        expected_labels = [
            "Repetitor ish unvoni", "Fan nomi", "O'rgatish til(lar)i", "Ism", "Familiya", "Tel raqami",
            "Elektron pochta", "Biznes ish vaqtlar"
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
        rep_unvon_input = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/div[1]/div[1]/input")
        subjects_dropdown = self.driver.find_element(By.XPATH,
                                                     "/html/body/main/div/main/div/div[2]/div[1]/div[2]/div/div[2]/div[1]")
        languages_label = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/div[1]/div[3]/label")
        name_input = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/div[1]/div[4]/input")
        phone_div = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/div[1]/div[6]/div")
        email_input = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/div[1]/div[7]/input")
        business_days_label = self.driver.find_element(By.XPATH,
                                                       "/html/body/main/div/main/div/div[2]/div[1]/div[8]/label")

        # 'aria-invalid'/'data-error'/'input-error' should remain true
        self.assertEqual(rep_unvon_input.get_attribute("aria-invalid"), "true")
        self.assertIn("input-error", subjects_dropdown.get_attribute("class"))
        self.assertEqual(languages_label.get_attribute("data-error"), "true")
        self.assertEqual(name_input.get_attribute("aria-invalid"), "true")
        self.assertEqual(phone_div.get_attribute("aria-invalid"), "true")
        self.assertEqual(email_input.get_attribute("aria-invalid"), "true")
        self.assertEqual(business_days_label.get_attribute("data-error"), "true")

    def test_03_form_valid_submission(self):
        """ Test for valid submission. """

        # == Fill in unvon name ==
        unvon_input = self.driver.find_element(By.NAME, "name")
        unvon_input.clear()
        unvon_input.send_keys("Django Teacher")

        # == Fill in subject name ==
        subjects_dropdown = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]")

        # Open dropdown
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", subjects_dropdown)
        time.sleep(0.5)
        self.wait.until(EC.element_to_be_clickable(subjects_dropdown)).click()

        # Retrieve options
        time.sleep(0.2)
        subject_options = self.driver.find_elements(By.XPATH,  "/html/body/main/div/main/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div")

        # Expected subjects
        expected_subjects = ['Adabiyot',
                             'Algebra',
                             'Android ilova ishlab chiqish',
                             'Arab tili',
                             'Arman tili',
                             'Astronomiya',
                             'Baraban',
                             'Bas-gitara',
                             'Biologiya',
                             'Biznes va menejment',
                             'Biznes-analitika',
                             'Biznes-strategiya',
                             'Buxgalteriya hisobi',
                             'C#',
                             'C++',
                             'CSS',
                             'Chex tili',
                             'Chizma',
                             'Chizmachilik',
                             'Design - 3D',
                             'Design - 3D',
                             'Falsafa',
                             'Fizika',
                             'Flutter',
                             'Fors tili',
                             'Fotosurat',
                             'Fransuz tili',
                             'Geografiya',
                             'Geometriya',
                             'Gitara',
                             'Grafik dizayn',
                             'HTML',
                             'Hind tili',
                             'IT loyiha boshqaruvi',
                             'Ijtimoiy fanlar',
                             'Informatika',
                             'Ingliz tili',
                             'Iqtisodiyot',
                             'Ishora tili',
                             'Ispan tili',
                             'Italyan tili',
                             'Java',
                             'JavaScript',
                             'Kimyo',
                             'Kontent marketingi',
                             'Kopirayterlik',
                             'Koreys tili',
                             'Kotlin',
                             'Lotin tili',
                             'Loyiha menejment',
                             "Ma'lumotlar bazasi",
                             "Ma'lumotlar tadqiqoti",
                             'Marketing',
                             'Matematika',
                             'Motion Design',
                             'Musiqa',
                             'Nemis tili',
                             "O'zbek tili",
                             'Ommaviy nutq',
                             'PHP',
                             'Pianino',
                             'Portugal tili',
                             'Produkt menejment',
                             'Psixologiya',
                             'Python',
                             'Rus tili',
                             'SEO',
                             'SMM/SMD',
                             'SQL',
                             'Saksofon',
                             'San’at',
                             'Skripka',
                             'Sotsiologiya',
                             'Sotuv kursi',
                             'Statistika',
                             "Sun'iy intellekt",
                             'Swift',
                             'Tarix',
                             'Tay tili',
                             'Tibbiyot',
                             'Trigonometriya',
                             'Turk tili',
                             'UX/UI',
                             'Veb-analitika',
                             'Veb-sayt ishlab chiqish',
                             'Video post-produktsiya',
                             'Xitoy tili',
                             'Yahudiy tili',
                             'Yapon tili',
                             'Yozish kursi',
                             'Yuridik xizmatlar',
                             'iOS ilova ishlab chiqish',
                             "Мa'lumotlar tahlili"]
        actual_subjects = [option.text for option in subject_options]
        self.assertEqual(sorted(expected_subjects), sorted(actual_subjects), "Subjects should be the same")

        # Choose random options
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", subjects_dropdown)
        random_subjects = random.sample(subject_options, 5)

        for subject in random_subjects:
            self.wait.until(EC.element_to_be_clickable(subject))
            self.driver.execute_script("arguments[0].click();", subject)

        # Close dropdown
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", subjects_dropdown)
        self.wait.until(EC.element_to_be_clickable(unvon_input)).click()


        # == Fill in languages ==
        languages_dropdown = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/div[1]/div[3]/button")

        # Open dropdown
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", languages_dropdown)
        self.wait.until(EC.element_to_be_clickable(languages_dropdown)).click()


        # Retrieve options
        time.sleep(0.2)
        language_options = self.driver.find_elements(By.XPATH, "/html/body/div/div/div/div/div/div")

        # Expected languages
        expected_langs = ['Ingliz tili', "O'zbek tili", 'Rus tili']
        actual_langs = [option.text for option in language_options]
        self.assertEqual(sorted(expected_langs), sorted(actual_langs), "Languages should be the same")

        # Choose random options
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", languages_dropdown)
        random_langs = random.sample(language_options, 2)

        for lang in random_langs:
            self.wait.until(EC.element_to_be_clickable(lang))
            self.driver.execute_script("arguments[0].click();", lang)

        # Close dropdown
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", languages_dropdown)
        self.wait.until(EC.element_to_be_clickable(languages_dropdown)).click()

        # == FIll in first name ==
        first_name_input = self.driver.find_element(By.NAME, "first_name")
        first_name_input.clear()
        first_name_input.send_keys("Test Name")

        # == FIll in last name ==
        last_name_input = self.driver.find_element(By.NAME, "last_name")
        last_name_input.clear()
        last_name_input.send_keys("Test Surname")

        # == Fill in phone input ==
        phone_input = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, '99 999')]")
        phone_input.clear()
        phone_input.send_keys("90 123 45 67")

        # # == Email fill in ==
        email_input = self.driver.find_element(By.NAME, "email")
        email_input.clear()
        email_input.send_keys(f"test_{random.randint(100,1000)}@email.com")

        # == FIll in business times ==
        random_days = random.sample(range(0,7), 3)

        # Locate day checkboxes
        day_chekboxes = self.driver.find_elements(By.XPATH, "/html/body/main/div/main/div/div[2]/div[1]/div[8]/div/div/div[1]/button[1]")

        for day in random_days:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", day_chekboxes[day])
            self.wait.until(EC.element_to_be_clickable(day_chekboxes[day]))
            self.driver.execute_script("arguments[0].click();", day_chekboxes[day])

        time.sleep(0.5)

        for day in random_days:
            for i in range(2):
                # Click dropdown
                target_dropdown = self.driver.find_element(By.XPATH, f"/html/body/main/div/main/div/div[2]/div[1]/div[8]/div/div[{day+1}]/div[2]/button[{i+1}]")
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
        self.assertEqual(title, "Yonda ilovasida repetitor akkauntini olish uchun quyidagi formani to‘ldiring:")

        # Locate the div
        address_div = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]")

        # Extract labels
        actual_labels = map(lambda label: self.extract_text_without_propagation(label),
                            address_div.find_elements(By.TAG_NAME, "label"))

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
        address_required_field = self.driver.find_element(By.XPATH,
                                                          "/html/body/main/div/main/div/div[2]/div[1]/div[1]/span")
        self.assertEqual(address_required_field.text, "Manzilni kiritish shart (latitude)")

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

    def test_07_specifics_required_fields(self):
        """ Test for benefits field present """

        # Check the title
        title = self.driver.find_element(By.TAG_NAME, "h1").text
        self.assertEqual(title, "Yonda ilovasida repetitor akkauntini olish uchun quyidagi formani to‘ldiring:")

        # Locate the div
        benefits_div = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]")

        # Extract labels
        actual_labels = map(lambda label: self.extract_text_without_propagation(label),
                            benefits_div.find_elements(By.TAG_NAME, "label"))

        # Check for all labels
        expected_labels = [ "Boshlanish sanasi",
                            'Diplom yoki Sertifikat fayli',
                            'Repetitor ish unvoni',
                            "Ta'lim muassasasi",
                            'Tugash sanasi' ]

        # Verify that labels match
        self.assertEqual(sorted(actual_labels), sorted(expected_labels), "Required fields are mismatched.")

    def test_08_specifics_empty_submission(self):
        """Test for empty submission."""

        # Click submit button
        submit_button = self.driver.find_element(By.XPATH, "//button[.//span[text()='Davom etish']]")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        self.wait.until(EC.element_to_be_clickable(submit_button))
        self.driver.execute_script("arguments[0].click();", submit_button)

        # Fields should still be empty and marked invalid
        university_name_input = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div/div/div[1]/div[1]/input")
        ish_unvon_input = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div/div/div[1]/div[2]/input")
        from_date_btn = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div/div/div[1]/div[3]/div[1]/button")
        to_date_btn = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div/div/div[1]/div[3]/div[2]/button")
        certificate_div = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div/div/div[1]/div[4]/div")

        # 'input-error' CSS selector, 'aria-invalid' attribute should be true
        self.assertEqual(university_name_input.get_attribute("aria-invalid"), "true")
        self.assertEqual(ish_unvon_input.get_attribute("aria-invalid"), "true")
        self.assertEqual(from_date_btn.get_attribute("aria-invalid"), "true")
        self.assertEqual(to_date_btn.get_attribute("aria-invalid"), "true")
        self.assertIn("input-error", certificate_div.get_attribute("class"))

    def test_09_specifics_valid_submission(self):
        """Test for valid submission."""

        # == Fill in university name ==
        university_name_input = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div/div/div[1]/div[1]/input")
        university_name_input.clear()
        university_name_input.send_keys("Test University")

        # == Fill in ish unvon ==
        ish_unvon_input = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div/div/div[1]/div[2]/input")
        ish_unvon_input.clear()
        ish_unvon_input.send_keys("Test Ish Unvoni")

        # == Fill in from date ==

        # Click date picker
        from_date_btn = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div/div/div[1]/div[3]/div[1]/button")
        self.wait.until(EC.element_to_be_clickable(from_date_btn)).click()

        # Wait till date picker opens
        time.sleep(0.5)

        # Retrieve option
        from_date_option = self.driver.find_element(By.XPATH, f"/html/body/div/div/div/div/div/table/tbody/tr/td/button[contains(text(), '{datetime.today().day-5}')]")
        self.wait.until(EC.element_to_be_clickable(from_date_option)).click()

        # Close date picker
        from_date_option.send_keys(Keys.ESCAPE)

        # == Fill in to date ==

        # Click date picker
        to_date_btn = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div/div/div[1]/div[3]/div[2]/button")
        self.wait.until(EC.element_to_be_clickable(to_date_btn)).click()

        # Wait till date picker opens
        time.sleep(0.5)

        # Retrieve option
        to_date_option = self.driver.find_element(By.XPATH, f"/html/body/div/div/div/div/div/table/tbody/tr/td/button[contains(text(), '{datetime.today().day+5}')]")
        self.wait.until(EC.element_to_be_clickable(to_date_option)).click()

        # Close date picker
        to_date_option.send_keys(Keys.ESCAPE)

        # == Upload file ==
        file_path = os.path.abspath("image.jpeg")
        upload_input = self.driver.find_element(By.ID, "certificate-0")
        upload_input.send_keys(file_path)

        # Check if the img is actually uploaded
        uploaded_p= self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div/div/div[1]/div[4]/div/div[2]/div[1]/p")))
        self.assertEqual(uploaded_p.text, "image.webp", "Image should be uploaded")

        # Click submit button
        submit_button = self.driver.find_element(By.XPATH, "//button[.//span[text()='Davom etish']]")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        self.wait.until(EC.element_to_be_clickable(submit_button))
        self.driver.execute_script("arguments[0].click();", submit_button)

    def test_10_image_required_fields(self):
        """Test for required fields present."""

        # Check the title
        title = self.driver.find_element(By.TAG_NAME, "h1").text
        self.assertEqual(title, "Yonda ilovasida repetitor akkauntini olish uchun quyidagi formani to‘ldiring:")

        # Property dropdown
        property_dropdown_div = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div[1]/div/div")
        self.assertEqual(property_dropdown_div.text, "Xususiyatini tanlang")

        # Locate the 'input' div
        input_div = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div[3]/div/div[2]")

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

        # 'Xususiyatlar' dropdown
        property_dropdown_div = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div[1]/div/div")
        self.assertIn("input-error", property_dropdown_div.get_attribute("class"), "Invalid input")

        # 'Rasm kiritish majburiy' should be visible
        image_required_warning = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div[3]/div/div[2]/p")
        self.assertEqual(image_required_warning.text, "Rasm kiritish majburiy", "Image should be uploaded")

    def test_12_image_valid_submission(self):
        """Test for valid submission."""

        # Locate 'Xususiyatlar' dropdown
        property_dropdown_div = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div[1]/div/div")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", property_dropdown_div)
        time.sleep(0.5)
        self.wait.until(EC.element_to_be_clickable(property_dropdown_div)).click()

        # Choose 3 random options
        property_options = self.driver.find_elements(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div[1]/div/div[2]/div[contains(concat(' ', normalize-space(@class), ' '), ' flex ')]")
        random_options = random.sample(property_options, 3)

        for option in random_options:
            self.driver.execute_script("arguments[0].click();", option)

        file_path = os.path.abspath("image.jpeg")

        # Image input
        upload_input = self.driver.find_element(By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div[3]/div/div[3]/input")
        upload_input.send_keys(file_path)

        # Check if the img is actually uploaded
        uploaded_img = self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div/main/div/div[2]/main/div/div[3]/div/div[2]/div/div/div/img")))
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
