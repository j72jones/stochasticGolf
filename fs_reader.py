from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# Load your CSV
df = pd.read_csv('shots.csv')  # Update with your file name

# Launch browser
driver = webdriver.Chrome()
driver.get("trackman-csv-export-20230807.Normalized.csv")


time.sleep(3)  # wait for page to load fully

# Loop through each row (shot)
for index, row in df.iterrows():
    # Wait a bit to ensure fields are ready
    time.sleep(1)

    # Find and fill in form fields
    driver.find_element(By.NAME, "ballSpeed").clear()
    driver.find_element(By.NAME, "ballSpeed").send_keys(str(row['Ball Speed']))

    driver.find_element(By.NAME, "verticalLaunchAngle").clear()
    driver.find_element(By.NAME, "verticalLaunchAngle").send_keys(str(row['Launch Angle']))

    driver.find_element(By.NAME, "spinRate").clear()
    driver.find_element(By.NAME, "spinRate").send_keys(str(row['Spin Rate']))

    driver.find_element(By.NAME, "azimuth").clear()
    driver.find_element(By.NAME, "azimuth").send_keys(str(row['Launch Direction']))

    driver.find_element(By.NAME, "sideSpin").clear()
    driver.find_element(By.NAME, "sideSpin").send_keys(str(row['Spin Axis']))

    driver.find_element(By.NAME, "backSpin").clear()
    driver.find_element(By.NAME, "backSpin").send_keys(str(row['backSpin']))

    # Click "Add Shot" button
    add_button = driver.find_element(By.XPATH, "//button[contains(text(),'Add Shot')]")
    add_button.click()

    time.sleep(1)  # wait for UI to catch up

print("All shots submitted. You can now manually click 'Export CSV' on the site.")
