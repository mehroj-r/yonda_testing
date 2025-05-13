from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestUtils:
    """Base class for all test classes to avoid code duplication."""

    @classmethod
    def setup_browser(cls, url, executable_path="./chromedriver"):
        """Set up the browser with the provided options."""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        service = Service(executable_path=executable_path)
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)

        cls.driver.maximize_window()
        cls.driver.get(url)
        cls.driver.implicitly_wait(5)
        cls.wait = WebDriverWait(cls.driver, 10)

        return cls.driver

    @staticmethod
    def click_link_test(driver, wait, target_element, target_link, exact_match=True):
        """Tests if clicking passed element redirects to that link in the same tab"""

        # Scroll into the element to avoid interception
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)

        # Capture current URL
        original_url = driver.current_url

        # Click the element when clickable
        wait.until(EC.element_to_be_clickable(target_element))
        driver.execute_script("arguments[0].click();", target_element)

        # Wait for URL to change
        wait.until(lambda d: d.current_url != original_url)

        # Assert the expected redirection
        current_url = driver.current_url
        result = False

        if exact_match:
            result = (current_url == target_link)
        else:
            result = current_url.startswith(target_link)

        # Navigate back and wait for document ready
        driver.back()
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        return result

    @staticmethod
    def click_external_link_test(driver, wait, target_element, target_link, exact_match=True):
        """Tests if clicking passed element opens the correct link in a new tab"""

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)

        current_window = driver.current_window_handle
        existing_windows = driver.window_handles

        # Click the element
        wait.until(EC.element_to_be_clickable(target_element))
        driver.execute_script("arguments[0].click();", target_element)

        # Wait for a new window/tab to open
        wait.until(lambda d: len(d.window_handles) > len(existing_windows))

        # Switch to the new window
        new_window = next(handle for handle in driver.window_handles if handle not in existing_windows)
        driver.switch_to.window(new_window)

        # Wait for document ready
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        # Assert the expected URL
        current_url = driver.current_url
        result = False
        if exact_match:
            result = (current_url == target_link)
        else:
            result = current_url.startswith(target_link)

        # Close the new tab and switch back
        driver.close()
        driver.switch_to.window(current_window)

        return result

    @staticmethod
    def extract_text_without_propagation(driver, tag):
        return driver.execute_script("""
                        let node = arguments[0];
                        let text = "";
                        for (let child of node.childNodes) {
                            if (child.nodeType === Node.TEXT_NODE)
                                text += child.textContent.trim();
                        }
                        return text;
                    """, tag)