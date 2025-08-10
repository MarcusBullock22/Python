from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function to log into a website
def login_to_website(url, username, password):
    options = Options()
    # Comment out headless for debugging if needed
    # options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    print("Initializing Chrome WebDriver...")
    driver = webdriver.Chrome(service=service, options=options)
    print("WebDriver initialized successfully.")

    try:
        print("Attempting to log in...")
        driver.get(url)
        
        # Accept cookies immediately after the page loads
        accept_cookies(driver)

        print("Waiting for login form to load...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "login"))
        )

        print("Login form is available, filling out login details...")
        username_field = driver.find_element(By.NAME, "login")
        password_field = driver.find_element(By.ID, "user_password")

        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        # Wait for the page to fully load after login
        print("Waiting for the page to load and checking for the redirection...")
        WebDriverWait(driver, 30).until(
            EC.url_to_be("https://www.fastweb.com/?from_login=true")
        )
        print("Redirected to the correct page.")

        # Now, attempt to click the "SEE MATCHES" button
        click_see_matches(driver)

        # Now, proceed with applying to scholarships
        click_view_buttons(driver)

        # Return the driver object for subsequent actions (scraping or others)
        return driver

    except Exception as e:
        print(f"Error occurred during login or subsequent actions: {e}")
        driver.quit()

# Function to handle the cookie consent prompt (if present)
def accept_cookies(driver):
    try:
        print("Checking for cookie prompt...")
        # Wait for the accept cookies button to appear and accept cookies
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
        )
        accept_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        accept_button.click()
        print("Cookies accepted.")
    except Exception as e:
        print("No cookie prompt appeared, or failed to accept cookies.")

# Function to click the "SEE MATCHES" button with hover and click
def click_see_matches(driver):
    try:
        print("Attempting to find 'SEE MATCHES' button...")

        # Refined XPath to match the button
        see_matches_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@class="my_matches button" and text()="SEE MATCHES"]'))
        )
        print("Found 'SEE MATCHES' button.")

        # Scroll down until the "SEE MATCHES" button is in view
        while not is_element_in_view(driver, see_matches_button):
            driver.execute_script("window.scrollBy(0, 100);")  # Scroll down by 300px
            time.sleep(1)  # Allow time for scrolling

        # Scroll to the button to make sure it's in view
        driver.execute_script("arguments[0].scrollIntoView();", see_matches_button)
        time.sleep(1)  # Allow page to settle

        # Hover over the "SEE MATCHES" button
        actions = ActionChains(driver)
        actions.move_to_element(see_matches_button).perform()
        print("Hovered over SEE MATCHES.")

        # Click on the "SEE MATCHES" button
        actions.click(see_matches_button).perform()
        print("Clicked on SEE MATCHES.")
        
        # Wait for the matched scholarships page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Matched Scholarships')]"))
        )
        print("Matched Scholarships page loaded.")
        
    except Exception as e:
        print(f"Error occurred while clicking 'SEE MATCHES': {e}")

# Function to check if the element is in the viewport
def is_element_in_view(driver, element):
    # Get the location of the element
    location = element.location
    size = element.size

    # Get the viewport's dimensions
    viewport_height = driver.execute_script("return window.innerHeight")
    viewport_width = driver.execute_script("return window.innerWidth")

    # Get the element's position in the viewport
    element_top = location['y']
    element_bottom = location['y'] + size['height']

    return element_top >= 0 and element_bottom <= viewport_height

# Function to scroll down the page and click on all "VIEW" buttons
def click_view_buttons(driver):
    try:
        # Find all "VIEW" buttons on the page
        view_buttons = driver.find_elements(By.XPATH, '//a[@class="view-application"]')

        if not view_buttons:
            print("No 'VIEW' buttons found.")
            return

        print(f"Found {len(view_buttons)} 'VIEW' buttons.")

        # Scroll down incrementally and click the "VIEW" button
        for button in view_buttons:
            # Scroll to the "VIEW" button
            driver.execute_script("arguments[0].scrollIntoView();", button)
            time.sleep(1)  # Allow page to settle

            # Click the "VIEW" button
            button.click()
            print(f"Clicked on VIEW for scholarship: {button.text}")

            # Wait for the next page to load (you can adjust the time as necessary)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "application-page"))  # Adjust if needed
            )

            # Navigate back to the previous page to continue applying to the next scholarship
            driver.back()
            time.sleep(2)  # Wait for the page to load

    except Exception as e:
        print(f"Error occurred while clicking 'VIEW': {e}")

# Example usage
if __name__ == "__main__":
    login_to_website(
        url="https://www.fastweb.com/login",  # Replace with the actual login page URL
        username="",  # Replace with your username
        password=""   # Replace with your password
    )
