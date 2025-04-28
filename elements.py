"""Selectors for searching html elements"""
staff_btn_selector = "a.staff-btn"
add_btn_selector = 'button.chdc-button__small.mdc-button--unelevated'
narrative_area_selector = 'header > div.sidebar__field-list app-text-field-editor-cell > div.cell-wrapped.editable'
narrative_input_selector = 'textarea[placeholder="Enter Narrative"]'
loctype_area_selector = 'section > div:nth-child(3) div.cell-wrapped.editable'
loctype_input_selector = "input.mat-mdc-input-element[placeholder='Search Location Type']"
actor1_area_selector = 'section > div:nth-child(7) div.cell-wrapped.editable'
actor1_input_selector = 'input.mat-mdc-input-element[placeholder="Search Actor 1 (Perpetrator)"]'
actor1_path_selector = 'section > div:nth-child(7) div.cell-options > div.path-preview'
actor2_area_selector = 'section > div:nth-child(8) div.cell-wrapped.editable'
actor2_input_selector = 'input.mat-mdc-input-element[placeholder="Search Actor 2 (Target)"]'
actor2_path_selector = 'section > div:nth-child(8) div.cell-options > div.path-preview'
act_area_selector = 'section > div:nth-child(9) div.cell-wrapped.editable'
act_input_selector = 'input.mat-mdc-input-element[placeholder="Search Act"]'
act_path_selector = 'section > div:nth-child(9) div.cell-options > div.path-preview'
act_attempted_selector = 'input[value="act-result:attempted"]'
source_area_selector = 'section > div:nth-child(19) div.cell-wrapped.editable'
source_input_selector = 'input.mat-mdc-input-element[placeholder="Search Source"]'
location_area_selector = 'section > div:nth-child(2) > div > app-select-editor-cell > div.cell-wrapped.editable'
location_li_selector = 'section > div:nth-child(2) ul > li[title="{title}"]'
latlon_area_selector = 'section > div:nth-child(4) > div > app-lat-lng-editor-cell > div.cell-wrapped.editable'
lat_input_selector = 'input.custom-lat-lng-element[placeholder="Latitude"]'
lon_input_selector = 'input.custom-lat-lng-element[placeholder="Longitude"]'
pi_area_selector = 'section > div:nth-child(12) > div > app-sheet-editor-cell > div.cell-wrapped.editable'
pi_btn_selector = 'section > div:nth-child(12) > div > app-sheet-editor-cell > div > div > button.chdc-select-suffix-button'
pi_actor_field_selector = 'chdc-sheets-dialog div.cheat-item.ng-star-inserted > div:nth-child(2) > div > app-select-editor-cell > div'
pi_type_field_selector = 'chdc-sheets-dialog div.cheat-item.ng-star-inserted > div:nth-child(3) div.row.cheat-row.ng-star-inserted > div:nth-child(1) > app-select-editor-cell > div'
pi_item_field_selector = 'chdc-sheets-dialog div.cheat-item.ng-star-inserted > div:nth-child(3) div.row.cheat-row.ng-star-inserted > div:nth-child(2) > app-select-editor-cell > div'
pi_save_btn_xpath ='//button[span[contains(text(), "Save")]]'
datetime_area_selector = 'div > app-datetime-editor-cell > div.cell-wrapped.editable'
calendar_button_selector = 'button:has(mat-icon[data-mat-icon-name="calendar"])'
month_year_choosing_selector = 'button[aria-label="Choose month and year"]'
year_button_selector = 'button[aria-label="{year}"]'
month_button_selector = 'button[aria-label="{month} {year}"]'
day_button_selector = 'button[aria-label="{month} {day}, {year}"]'
hour_field_selector = 'div.datetime-picker-container > div.timepicker-flex-container > select'
apply_date_selector = 'button[data-testid="datepicker-apply-button"]'
submit_button_selector = 'button[data-testid="submit-button"]'
simple_li_selector = 'li[title="{title}"]'
splash_screen_selector = 'chdc-splash-screen.ng-star-inserted'
email_field_selector = 'input.form-control[placeholder="Enter your INSO email address"]'
pass_field_selector = 'input.form-control[type="password"]'
chdc_title_text = "INSO CHDC"
next_btn_selector = 'input.win-button[type="submit"]'
modal_window_selector = 'mat-dialog-container[aria-modal="true"]'
modal_close_btn_selector = 'chdc-info-dialog > div > header > button.mat-icon-button'
radio_group_selector = 'div.editable.valid > div.radio-options > mat-radio-group'
incident_id_selector = 'header > div.sidebar__title > span.status-badge.status-badge--incomplete'

pi_actors_path = {
    "Other General Public": ["General Public"],
}

perpetrators_path = {
	"Russian Army": [
			"Foreign Government Forces",
			"Single Foreign Government Forces",
			"Russia",
            "Russian Army"
	],
	"Russian Airforce": [
			"Foreign Government Forces",
			"Single Foreign Government Forces",
			"Russia",
            "Russian Airforce"
	],
}

acts_path = {
    "Artillery/Other": [
        "Attack",
        "Artillery, Rockets & Missiles",
        "Other"
    ],
    "Airstrike": [
        "Attack",
        "Platforms",
        "Airstrike"
    ],
    "Rockets & Missiles": [
        "Attack",
        "Artillery, Rockets & Missiles",
        "Rockets & Missiles"
    ],
    "Long Range Attack": [
        "Attack",
        "Platforms",
        "Drone",
        "Long Range Attack"
    ],
    "Short Range Attack": [
        "Attack", "Platforms", "Drone", "Short Range Attack"
    ],
    "Light Weapons": [
        "Attack", "Small Arms & Light Weapons", "Light Weapons"
    ],
    "Artillery": [
        "Attack", "Artillery, Rockets & Missiles", "Artillery"
    ],
    "Helicopter": [
        "Attack", "Platforms", "Helicopter"
    ],
    "Fighting Vehicle": [
        "Attack", "Platforms", "Fighting Vehicle"
    ],
}
