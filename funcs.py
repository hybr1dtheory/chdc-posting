from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import elements as el


def login(driver: Chrome) -> None:
    """Function for authentication to CHDC"""
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.staff_btn"))
    ).click()


def start_input(driver: Chrome) -> None:
    """Function to start adding new incedent"""
    WebDriverWait(driver, 15).until(
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
    driver.execute_script("arguments[0].blur();", area_to_click)


def set_datetime(driver: Chrome, year: int, month: int, day: int,
                hour=0, minute=0, write_time=True) -> None:
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
    # select hours and minutes or press 'remove time'
    if not write_time:
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, el.remove_time_button_xpath)
            )
        ).click()
    else:
        hour_field = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, el.hour_field_selector)
            )
        )
        hour_field.clear()
        hour_field.send_keys(str(hour))
        minute_field = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, el.minute_field_selector)
            )
        )
        minute_field.clear()
        minute_field.send_keys(str(minute))
    # Press "Apply" button
    apply_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, el.apply_date_xpath)
        )
    )
    apply_button.click()
    driver.execute_script("arguments[0].blur();", area_to_click)


def set_location(driver: Chrome, obl: str, rai:str, hrom:str, settl="N/A settlement") -> None:
    """function for filling location field"""
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
    """function for filling location type field"""
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


def set_perpetrator(driver: Chrome, actor: str) -> None:
    """function for filling actor 1 field"""
    area_to_click = driver.find_element(By.CSS_SELECTOR, el.actor1_area_selector)
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})",
        area_to_click
    )
    wait = WebDriverWait(driver, 3)
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
    wait = WebDriverWait(driver, 3)
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


def set_act(driver: Chrome, act: str) -> None:
    """function for filling act field"""
    area_to_click = driver.find_element(By.CSS_SELECTOR, el.act_area_selector)
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})",
        area_to_click
    )
    wait = WebDriverWait(driver, 3)
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
    driver.execute_script("arguments[0].blur();", area_to_click)


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


def submit_data(driver: Chrome) -> None:
    """"""
    submit_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, el.submit_button_selector)
        )
    )
    submit_btn.click()
