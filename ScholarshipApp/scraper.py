from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to scrape scholarships after login
def scrape_scholarships(driver):
    try:
        print("Navigating to the scholarships pages...")

        # Navigate to the scholarship browsing page
        driver.get("https://www.fastweb.com/college-scholarships/featured-scholarships")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "scholarship-item"))  # Adjust class name
        )

        # Scrape the scholarships
        scholarships = driver.find_elements(By.CLASS_NAME, "scholarship-item")
        if scholarships:
            print(f"Found {len(scholarships)} browse scholarships.")
        else:
            print("No browse scholarships found.")

        # Navigate to the matched scholarships page
        driver.get("https://www.fastweb.com/college-scholarships/scholarships?filter=Matched")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "match-item"))  # Adjust class name
        )

        matched_scholarships = driver.find_elements(By.CLASS_NAME, "scholarship-item")
        if matched_scholarships:
            print(f"Found {len(matched_scholarships)} matched scholarships.")
        else:
            print("No matched scholarships found.")

        # Combine both lists of scholarships
        all_scholarships = scholarships + matched_scholarships

        # Return all scholarships
        return all_scholarships

    except Exception as e:
        print(f"Error occurred while scraping scholarships: {e}")
        return []  # Return an empty list if there's an error
