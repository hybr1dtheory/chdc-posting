"""Module with all functionality to iteract with webpage 
with different types of fields and to enter data into it."""
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import elements as el
import config as cfg


def complete_mfa(driver: Chrome) -> None:
    """Function to go through multifactor auth"""
    email = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, el.email_field_selector)
        )
    )
    email.click()
    email.clear()
    email.send_keys(cfg.user_email)
    submit_btn = driver.find_element(By.CSS_SELECTOR, el.next_btn_selector)
    submit_btn.click()
    pswd = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, el.pass_field_selector)
        )
    )
    pswd.click()
    pswd.clear()
    pswd.send_keys(cfg.user_pass)
    submit_btn = driver.find_element(By.CSS_SELECTOR, el.next_btn_selector)
    submit_btn.click()
    # waiting to enter code in auth app by hand
    WebDriverWait(driver, 30).until(
        EC.url_to_be(cfg.mfa_complete_url)
    )
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.next_btn_selector)
        )
    ).click()
    WebDriverWait(driver, 15).until(
        EC.title_is(el.chdc_title_text)
    )


def login(driver: Chrome) -> None:
    """Function for authentication to CHDC"""
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.staff_btn_selector)
        )
    ).click()
    # check if MFA needed by url
    WebDriverWait(driver, 10).until(
        EC.url_changes(cfg.target_url)
    )
    time.sleep(5)
    if EC.url_contains(cfg.chdc_db_url):
        return
    elif EC.url_contains(cfg.mfa_url):
        complete_mfa(driver)
    else:
        raise ValueError(f"Unknown page: {driver.current_url}")


def start_input(driver: Chrome) -> None:
    """Function to start adding new incedent"""
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, el.add_btn_selector)
        )
    )
    # wait for invisibility of the loading animation screen
    wait.until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, el.splash_screen_selector)
        )
    )
    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, el.add_btn_selector))
    ).click()


def enter_narrative(driver: Chrome, text: str) -> None:
    """Function for filling the narrative textarea.
    firstly we must to click on the wrapper to have access to the textarea,
    then find the textarea after activating, click and fill it."""
    area_to_click = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.narrative_area_selector)
        )
    )
    area_to_click.click()
    narrative_textarea = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, el.narrative_input_selector)
        )
    )
    narrative_textarea.click()
    narrative_textarea.clear()
    narrative_textarea.send_keys(text)
    # un-focus the element
    driver.execute_script("arguments[0].blur();", area_to_click)


def set_datetime(
        driver: Chrome, year: int, month: int,
        day: int, hour=0, write_time=True
    ) -> None:
    """function for selecting the date and time from calendar"""
    # dict for convert month number to month name
    month_name = {
        1: 'January', 2: 'February', 3: 'March',
        4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8: 'August', 9: 'September',
        10: 'October', 11: 'November', 12: 'December'
    }
    # find and scroll to the target area
    area_to_click = driver.find_element(By.CSS_SELECTOR, el.datetime_area_selector)
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})",
        area_to_click
    )
    # set waiting time
    wait = WebDriverWait(driver, 3)
    # click on the field to start input
    wait.until(
        EC.element_to_be_clickable(area_to_click)
    ).click()
    # open the pop-up for date and time selecting
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.calendar_button_selector)
        )
    ).click()
    # click for selecting month and year
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.month_year_choosing_selector)
        )
    ).click()
    # select the year
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.year_button_selector.format(year=year))
        )
    ).click()
    # select the month
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
            el.month_button_selector.format(month=month_name[month], year=year))
        )
    ).click()
    # select the day
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
            el.day_button_selector.format(month=month_name[month], day=day, year=year))
        )
    ).click()
    # select hours if needed
    if write_time:
        hour_field = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, el.hour_field_selector)
            )
        )
        select_time = Select(hour_field)
        select_time.select_by_value(str(hour))
        
    # Press "Apply" button
    apply_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.apply_date_selector)
        )
    )
    apply_button.click()
    driver.execute_script("arguments[0].blur();", area_to_click)


def set_location(
        driver: Chrome, obl: str, rai:str, hrom:str, settl="N/A settlement"
    ) -> None:
    """function for filling the location field"""
    area_to_click = driver.find_element(By.CSS_SELECTOR, el.location_area_selector)
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})",
        area_to_click
    )
    wait = WebDriverWait(driver, 3)
    wait.until(
        EC.element_to_be_clickable(area_to_click)
    )
    area_to_click.click()
    # select 'Ukraine' and click
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.location_li_selector.format(title="Ukraine"))
        )
    ).click()
    # oblast selecting
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.location_li_selector.format(title=obl))
        )
    ).click()
    # raion selecting
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.location_li_selector.format(title=rai))
        )
    ).click()
    # hromada selecting
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.location_li_selector.format(title=hrom))
        )
    ).click()
    # settlement selecting
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.location_li_selector.format(title=settl))
        )
    ).click()
    driver.execute_script("arguments[0].blur();", area_to_click)


def set_location_type(driver: Chrome, loctype: str) -> None:
    """function for filling the location type field"""
    area_to_click = driver.find_element(By.CSS_SELECTOR, el.loctype_area_selector)
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})",
        area_to_click
    )
    area_to_click.click()
    WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.simple_li_selector.format(title=loctype))
        )
    ).click()
    driver.execute_script("arguments[0].blur();", area_to_click)


def set_coordinates(driver: Chrome, lat: float, lon: float) -> None:
    """function for filling coordinates"""
    area_to_click = driver.find_element(By.CSS_SELECTOR, el.latlon_area_selector)
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})",
        area_to_click
    )
    area_to_click.click()
    wait = WebDriverWait(driver, 3)
    lat_field = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.lat_input_selector)
        )
    )
    lat_field.click()
    lat_field.clear()
    lat_field.send_keys(str(lat))
    lon_field = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.lon_input_selector)
        )
    )
    lon_field.click()
    lon_field.clear()
    lon_field.send_keys(str(lon))
    driver.execute_script("arguments[0].blur();", area_to_click)


def set_perpetrator(driver: Chrome, actor: str) -> None:
    """function for filling actor 1 field"""
    area_to_click = driver.find_element(By.CSS_SELECTOR, el.actor1_area_selector)
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})",
        area_to_click
    )
    wait = WebDriverWait(driver, 5)
    wait.until(
        EC.element_to_be_clickable(area_to_click)
    )
    area_to_click.click()
    actor_field = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.actor1_input_selector)
        )
    )
    actor_field.click()
    actor_field.clear()
    actor_field.send_keys(actor)
    if actor != "Unknown Actor":
        wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, el.actor1_path_selector)
            )
        )
    driver.execute_script("arguments[0].blur();", actor_field)


def set_target(driver: Chrome, actor: str) -> None:
    """function for filling actor 2 field"""
    area_to_click = driver.find_element(By.CSS_SELECTOR, el.actor2_area_selector)
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})",
        area_to_click
    )
    wait = WebDriverWait(driver, 5)
    wait.until(
        EC.element_to_be_clickable(area_to_click)
    )
    area_to_click.click()
    actor_field = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, el.actor2_input_selector))
    )
    actor_field.click()
    actor_field.clear()
    actor_field.send_keys(actor)
    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, el.actor2_path_selector)
        )
    )
    driver.execute_script("arguments[0].blur();", actor_field)


def set_act(driver: Chrome, act: str, is_attempted = False) -> None:
    """function for filling an act field"""
    area_to_click = driver.find_element(By.CSS_SELECTOR, el.act_area_selector)
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})",
        area_to_click
    )
    wait = WebDriverWait(driver, 5)
    wait.until(
        EC.element_to_be_clickable(area_to_click)
    )
    area_to_click.click()
    act_field = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, el.act_input_selector))
    )
    act_field.click()
    act_field.clear()
    act_field.send_keys(act)
    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, el.act_path_selector)
        )
    )
    if is_attempted:
        set_act_attempted(driver)
    driver.execute_script("arguments[0].blur();", area_to_click)


def set_act_attempted(driver: Chrome) -> None:
    """function to click on the 'attempted' checkbox"""
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, el.radio_group_selector)
        )
    )
    elem = driver.find_element(By.CSS_SELECTOR, el.act_attempted_selector)
    elem.click()


def set_source(driver: Chrome, src="INSO") -> None:
    """function for filling source field"""
    area_to_click = driver.find_element(
        By.CSS_SELECTOR, el.source_area_selector
    )
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})",
        area_to_click
    )
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(area_to_click)
    )
    area_to_click.click()
    WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.simple_li_selector.format(title=src))
        )
    ).click()
    driver.execute_script("arguments[0].blur();", area_to_click)


def submit_data(driver: Chrome) -> str:
    """push the 'submit' button to send data
    and reurns an incident id in database (str)"""
    id_span = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, el.incident_id_selector)
        )
    )
    incident_id = id_span.text
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.submit_button_selector)
        )
    ).click()
    return incident_id
