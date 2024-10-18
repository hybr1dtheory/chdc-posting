"""This module is designed to automate data entry into a web form
with fields of several types (text, datetime, drop-down list)"""
from selenium.webdriver.chrome.options import Options
import logging
import pandas as pd
import funcs as fn
from config import profile_path, profile_name, target_url
from datetime import datetime


def write_incident(driver: fn.Chrome, row) -> None:
    """This function step by step calls all functions to add incident"""
    fn.start_input(driver)
    fn.enter_narrative(driver, row["Narrative"])
    fn.set_datetime(
        driver, row["Date"].year, row["Date"].month,
        row["Date"].day, write_time=False
    )
    fn.set_location(
        driver, obl=row["Oblast"], rai=row["Raion"],
        hrom=row["Hromada"], settl=row["Settlement"]
    )
    fn.set_location_type(driver, row["Location type"])
    fn.set_perpetrator(driver, row["Actor 1"])
    fn.set_target(driver, row["Actor 2"])
    fn.set_act(driver, row["Act"])
    fn.submit_data(driver)
    driver.refresh()


# define and configurate the webdriver
chrome_options = Options()
chrome_options.add_argument(fr'user-data-dir={profile_path}')
chrome_options.add_argument(fr"--profile-directory={profile_name}")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--start-maximized")  # open driver in maximized window
chrome_options.add_argument("--kiosk")  # fullscreen mode for the webpage
chrome_options.add_argument("zoom=0.5")  # set zoom to 50%
driver = fn.Chrome(options=chrome_options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    'source': '''delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;'''
})

logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs.txt', encoding='utf-8', level=logging.INFO)
try:
    logger.info(f"{datetime.now()} Started")
    file_path = 'incidents.xlsx'  # file with incidents data
    df = pd.read_excel(file_path)
    driver.get(target_url)
    fn.login(driver)
    for i, r in df.iterrows():
        logger.info(f"Incident {i+1} writing...")
        write_incident(driver, r)
        logger.info(f"ADDED {i+1}")
    logger.info(f"{datetime.now()} Finished\n\n")
except Exception as e:
    logger.exception(f"Error during execution: {e}")
    print(f"Error during execution: {e}")
finally:
    driver.quit()
