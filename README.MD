# 🧪 Automated Testing for [yonda.uz](https://yonda.uz)

> End-to-end UI test automation using **Python** and **Selenium WebDriver**

---

## 🚀 Overview

This project automates UI testing for the **yonda.uz** web platform using Selenium in Python. It includes modular page objects, structured test cases, and utility helpers for maintainable test execution.

---

## 🧰 Tech Stack

- **Language**: Python
- **Automation Framework**: Selenium WebDriver
- **Test Runner**: `unittest`
- **IDE**: PyCharm (recommended)
- **Browser Driver**: ChromeDriver

---

## 📁 Project Structure
```
SeleniumProject/
│
├── BasePageTest.py # Base test class for shared setup/teardown
├── MainPageTest.py # Tests for main/home page
├── PartnerPageTest.py # Partner section tests
├── RegisterBusinessPageTest.py # Business registration flow tests
├── RegisterRepetitorPageTest.py # Repetitor registration flow tests
├── SearchPageTest.py # Search functionality tests
│
├── TestUtils.py # Common utility functions
├── chromedriver # Chrome WebDriver executable
├── main.py # Script to run all test classes one by one
└── .gitignore
```

---

## ▶️ Running Tests

Make sure you have all dependencies installed and `chromedriver` is in your project root or PATH.

### ✅ Run all tests sequentially:
```bash
python main.py
```
