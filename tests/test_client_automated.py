"""
USIU G6 Automated Client Test Suite
====================================
Automated browser tests for frontend functionality using Selenium WebDriver.

This allows running client tests from the terminal without manual browser interaction.
"""

import unittest
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

# Add server to path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
server_dir = os.path.join(parent_dir, 'server')
sys.path.insert(0, server_dir)


class TestClientAutomated(unittest.TestCase):
    """Automated browser tests for client-side functionality"""

    @classmethod
    def setUpClass(cls):
        """Set up Chrome driver once for all tests"""
        print("\n" + "="*60)
        print("USIU G6 AUTOMATED CLIENT TEST SUITE")
        print("="*60 + "\n")
        print("⚙️  Setting up Chrome WebDriver...")
        
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.implicitly_wait(10)
            cls.base_url = "http://localhost:5000"
            print("✅ Chrome WebDriver initialized\n")
        except Exception as e:
            print(f"❌ Error: Could not initialize Chrome WebDriver")
            print(f"   Make sure Chrome and ChromeDriver are installed")
            print(f"   Error: {e}\n")
            raise

    @classmethod
    def tearDownClass(cls):
        """Close browser after all tests"""
        if hasattr(cls, 'driver'):
            cls.driver.quit()
            print("\n✅ Browser closed")

    def test_01_homepage_loads(self):
        """Test that homepage loads successfully"""
        print("▶️  Test 1: Homepage loads...")
        try:
            self.driver.get(self.base_url)
            self.assertIn("USIU G6", self.driver.title)
            print("   ✅ PASSED: Homepage loaded successfully\n")
        except Exception as e:
            print(f"   ❌ FAILED: {e}\n")
            raise

    def test_02_navigation_exists(self):
        """Test that navigation menu exists"""
        print("▶️  Test 2: Navigation menu exists...")
        try:
            self.driver.get(self.base_url)
            nav = self.driver.find_element(By.CLASS_NAME, "nav-links")
            self.assertIsNotNone(nav)
            print("   ✅ PASSED: Navigation menu found\n")
        except Exception as e:
            print(f"   ❌ FAILED: {e}\n")
            raise

    def test_03_login_page_accessible(self):
        """Test that login page is accessible"""
        print("▶️  Test 3: Login page accessible...")
        try:
            self.driver.get(f"{self.base_url}/login.html")
            self.assertIn("Login", self.driver.title)
            email_field = self.driver.find_element(By.ID, "email")
            password_field = self.driver.find_element(By.ID, "password")
            self.assertIsNotNone(email_field)
            self.assertIsNotNone(password_field)
            print("   ✅ PASSED: Login page loads with form fields\n")
        except Exception as e:
            print(f"   ❌ FAILED: {e}\n")
            raise

    def test_04_signup_page_accessible(self):
        """Test that signup page is accessible"""
        print("▶️  Test 4: Signup page accessible...")
        try:
            self.driver.get(f"{self.base_url}/signup.html")
            self.assertIn("Create", self.driver.title)
            form = self.driver.find_element(By.ID, "signupForm")
            self.assertIsNotNone(form)
            print("   ✅ PASSED: Signup page loads with form\n")
        except Exception as e:
            print(f"   ❌ FAILED: {e}\n")
            raise

    def test_05_contact_page_accessible(self):
        """Test that contact page is accessible"""
        print("▶️  Test 5: Contact page accessible...")
        try:
            self.driver.get(f"{self.base_url}/contact.html")
            form = self.driver.find_element(By.ID, "contactForm")
            self.assertIsNotNone(form)
            print("   ✅ PASSED: Contact page loads with form\n")
        except Exception as e:
            print(f"   ❌ FAILED: {e}\n")
            raise

    def test_06_mobile_menu_toggle_exists(self):
        """Test that mobile menu toggle exists"""
        print("▶️  Test 6: Mobile menu toggle exists...")
        try:
            self.driver.get(self.base_url)
            toggle = self.driver.find_element(By.ID, "menu-toggle")
            self.assertIsNotNone(toggle)
            print("   ✅ PASSED: Mobile menu toggle found\n")
        except Exception as e:
            print(f"   ❌ FAILED: {e}\n")
            raise

    def test_07_form_validation_attributes(self):
        """Test that forms have proper validation"""
        print("▶️  Test 7: Form validation attributes...")
        try:
            self.driver.get(f"{self.base_url}/login.html")
            email_field = self.driver.find_element(By.ID, "email")
            password_field = self.driver.find_element(By.ID, "password")
            
            # Check required attributes
            self.assertEqual(email_field.get_attribute("required"), "true")
            self.assertEqual(password_field.get_attribute("required"), "true")
            self.assertEqual(email_field.get_attribute("type"), "email")
            print("   ✅ PASSED: Form validation attributes correct\n")
        except Exception as e:
            print(f"   ❌ FAILED: {e}\n")
            raise

    def test_08_protected_pages_exist(self):
        """Test that protected pages exist"""
        print("▶️  Test 8: Protected pages exist...")
        try:
            protected_pages = ['our-work.html', 'pricing.html', 'our-team.html', 'about.html']
            for page in protected_pages:
                self.driver.get(f"{self.base_url}/{page}")
                # Should either load or redirect to login
                self.assertIn(self.driver.current_url, 
                             [f"{self.base_url}/{page}", f"{self.base_url}/login.html"])
            print("   ✅ PASSED: All protected pages exist\n")
        except Exception as e:
            print(f"   ❌ FAILED: {e}\n")
            raise

    def test_09_css_loaded(self):
        """Test that CSS stylesheets are loaded"""
        print("▶️  Test 9: CSS stylesheets loaded...")
        try:
            self.driver.get(self.base_url)
            # Check if stylesheet link exists
            stylesheets = self.driver.find_elements(By.CSS_SELECTOR, 'link[rel="stylesheet"]')
            self.assertGreater(len(stylesheets), 0)
            print("   ✅ PASSED: CSS stylesheets found\n")
        except Exception as e:
            print(f"   ❌ FAILED: {e}\n")
            raise

    def test_10_javascript_loaded(self):
        """Test that JavaScript files are loaded"""
        print("▶️  Test 10: JavaScript files loaded...")
        try:
            self.driver.get(self.base_url)
            scripts = self.driver.find_elements(By.TAG_NAME, 'script')
            self.assertGreater(len(scripts), 0)
            print("   ✅ PASSED: JavaScript files found\n")
        except Exception as e:
            print(f"   ❌ FAILED: {e}\n")
            raise


def check_server_running():
    """Check if Flask server is running"""
    import requests
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        return True
    except:
        return False


def run_automated_tests():
    """Run all automated client tests"""
    print("\n" + "="*60)
    print("CHECKING PREREQUISITES")
    print("="*60 + "\n")
    
    # Check if server is running
    print("🔍 Checking if Flask server is running...")
    if not check_server_running():
        print("❌ Error: Flask server is not running on http://localhost:5000")
        print("   Please start the server first:")
        print("   cd server && python app.py\n")
        return False
    print("✅ Server is running\n")
    
    # Check if Chrome/ChromeDriver is available
    print("🔍 Checking for Chrome and ChromeDriver...")
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.quit()
        print("✅ Chrome and ChromeDriver are available\n")
    except Exception as e:
        print("❌ Error: Chrome or ChromeDriver not found")
        print("   Install with: pip install selenium")
        print("   And download ChromeDriver from: https://chromedriver.chromium.org/\n")
        print("   Alternative: Run manual tests by opening test_client.html in browser\n")
        return False
    
    # Run tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestClientAutomated)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    print("="*60 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_automated_tests()
    sys.exit(0 if success else 1)
