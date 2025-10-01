from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
)
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

import time
import threading
import os
import psutil


def set_up_driver_instance():
    """To create and return a webdriver object with disabled gpu and headless"""

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'

    chrome_options = webdriver.ChromeOptions()  # Google Chrome
    # chrome_options = webdriver.EdgeOptions()      # Microsoft Edge
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--headless")

    # to stop printing error messages to the console
    chrome_options.add_argument("--log-level=3")
    # chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--disable-extensions")

    # prefs={'profile.default_content_setting_values': {'images': 2, 'javascript': 2}}
    # prefs = {"profile.managed_default_content_settings.images": 2, "profile.default_content_setting_values.javascript": 2}
    prefs = {
        "profile.default_content_setting_values": {
            "images": 2,
            "stylesheet": 2,
            "plugins": 2,
            "popups": 2,
            "geolocation": 2,
            "notifications": 2,
            "auto_select_certificate": 2,
            "fullscreen": 2,
            "mouselock": 2,
            "mixed_script": 2,
            "media_stream": 2,
            "media_stream_mic": 2,
            "media_stream_camera": 2,
            "protocol_handlers": 2,
            "ppapi_broker": 2,
            "automatic_downloads": 2,
            "midi_sysex": 2,
            "push_messaging": 2,
            "ssl_cert_decisions": 2,
            "metro_switch_to_desktop": 2,
            "protected_media_identifier": 2,
            "app_banner": 2,
            "site_engagement": 2,
            "durable_storage": 2,
        }
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # chrome_options.add_argument("--disable-blink-features")
    # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # chrome_options.add_argument('disable-infobars')

    # emulate a mobile device
    # mobile_emulation = { "deviceName": "Nexus 5" }
    #     mobile_emulation = {
    #    "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
    #    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
    #    "clientHints": {"platform": "Android", "mobile": True} }
    #     chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    # To rotate the user agent in order to avoid detection
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    # print(driver.execute_script("return navigator.userAgent;"))
    return webdriver.Chrome(options=chrome_options)  # Google Chrome
    # return webdriver.Edge(options=chrome_options)       # Microsoft Edge


def get_teams_scores(browser, current_n, full_results_history: dict) -> dict:
    events = browser.find_elements(
        By.CSS_SELECTOR, '[class="history-container ng-star-inserted"]'
    )[current_n * 5 :]

    # print("events: ", len(events))
    # full_results_history = {}
    date = ""
    for event in events:
        week = event.find_element(
            By.CSS_SELECTOR, '[class="event-block-id ng-star-inserted"]'
        ).text
        date = event.find_element(By.CSS_SELECTOR, '[class="event-block-date"]').text
        print(week, date)
        # league_id = heading.find_element(By.CSS_SELECTOR, 'span').text
        if week == "Week 34":
            if full_results_history != {}:
                print_both(full_results_history)
                # print_both(f"\n{date.text}\n\n")
                print_both(f"{date}\n")
            full_results_history = {}
            print("new league")
        full_results_history[week] = {}
        week_result = event.find_element(By.CSS_SELECTOR, '[class="panel-body"]')
        matches_in_week_result = week_result.find_elements(
            By.CSS_SELECTOR, '[class="ng-star-inserted"]'
        )
        for match in matches_in_week_result:
            h_team = match.find_element(
                By.CSS_SELECTOR, '[class="teamA flex-col"]'
            ).text
            a_team = match.find_element(
                By.CSS_SELECTOR, '[class="teamB flex-col"]'
            ).text
            score = match.find_element(
                By.CSS_SELECTOR, '[class="flex-col match-result-score p-1"'
            ).text
            try:
                match.click()
            except ElementClickInterceptedException:
                print("An ElementClickInterceptedException occured")
                browser.execute_script(
                    'arguments[0].scrollIntoView({block: "center", inline: "center"});',
                    match,
                )
                match.click()

            won_contents = match.find_element(
                By.CSS_SELECTOR, '[class="flex-row p-1 won-markets ng-star-inserted"]'
            )

            # # To find the won outcome based
            contents = won_contents.find_elements(
                By.CSS_SELECTOR, '[class="market-name"]'
            )
            for outcome in contents:
                if outcome.text.strip() == "HALF TIME/FULL TIME":
                    next_sibiling = outcome.find_element(
                        By.XPATH, "following-sibling::*[1]"
                    )
                    ht_ft_outcome = next_sibiling.text.split(":")
                    ht_ft, ht_ft_odd = (
                        ht_ft_outcome[0].strip(),
                        ht_ft_outcome[1].strip(),
                    )
                elif outcome.text.strip() == "CORRECT SCORE":
                    next_sibiling = outcome.find_element(
                        By.XPATH, "following-sibling::*[1]"
                    )
                    cs_outcome = next_sibiling.text.split(":")
                    cs, cs_odd = cs_outcome[0].strip(), cs_outcome[1].strip()
                    break

            full_results_history[week][f"{h_team} - {a_team}"] = {
                "correct_score": [cs, cs_odd],
                "ht/ft": [ht_ft, ht_ft_odd],
            }

            match.click()
    return [full_results_history, date]


def print_both(*args):
    """To print on the terminal as well as an output file"""
    with open("data/data_dv_sam.txt", "at") as file:
        to_print = " ".join([str(arg) for arg in args])
        # print(to_print)
        print(to_print, file=file)
        # file.write(to_print)


# print_both('""duhjndjbjcxhvbzxh')


def filter_history(browser, filter_date: str, filter_time: str):
    import calendar

    if filter_date != None:
        # filter function
        # Set the begining date for filter
        print(filter_date)
        filter_date = filter_date.split("/")
        print(filter_date)
        month_to_search = calendar.month_name[int(filter_date[1])]
        day_to_search = filter_date[0]
        prev_month = browser.find_element(
            By.CSS_SELECTOR, '[class="ui-datepicker-prev-icon pi pi-chevron-left"]'
        )
        # next_month = browser.find_element(
        #     By.CSS_SELECTOR,
        #     '[class="ui-datepicker-next ui-corner-all ng-tns-c13-62 ng-star-inserted"]',
        # )
        current_month = browser.find_element(
            By.CSS_SELECTOR,
            '[class="ui-datepicker-title"]',
        ).text.split()[0]
        while current_month != month_to_search.upper():
            prev_month.click()
            prev_month = browser.find_element(
                By.CSS_SELECTOR, '[class="ui-datepicker-prev-icon pi pi-chevron-left"]'
            )
            current_month = browser.find_element(
                By.CSS_SELECTOR,
                '[class="ui-datepicker-title"]',
            ).text.split()[0]
        # min_date = date_input.get_attribute("min")
        time.sleep(1)
        available_days = browser.find_elements(By.CSS_SELECTOR, ".ui-state-default")
        # print(len(available_days))
        for day in available_days:
            if int(day.text.strip()) == int(day_to_search):
                day.click()
                break

        time.sleep(1)
        # Set the filter time
        time_input_h = browser.find_element(By.CSS_SELECTOR, '[class="ui-hour-picker"]')
        # h_increase_btn = time_input_h.find_element(
        #     By.CSS_SELECTOR, '[class="pi pi-chevron-up"]'
        # )
        h_decrease_btn = time_input_h.find_element(
            By.CSS_SELECTOR, '[class="pi pi-chevron-down"]'
        )

        time_input_m = browser.find_element(
            By.CSS_SELECTOR, '[class="ui-minute-picker"]'
        )
        # m_increase_btn = time_input_m.find_element(
        #     By.CSS_SELECTOR, '[class="pi pi-chevron-up"]'
        # )
        m_decrease_btn = time_input_m.find_element(
            By.CSS_SELECTOR, '[class="pi pi-chevron-down"]'
        )
        # set the h input
        while time_input_h.text != filter_time.split(":")[0]:
            h_decrease_btn.click()
            time_input_h = browser.find_element(
                By.CSS_SELECTOR, '[class="ui-hour-picker"]'
            )

        # set the m input
        while time_input_m.text != filter_time.split(":")[1]:
            m_decrease_btn.click()
            time_input_m = browser.find_element(
                By.CSS_SELECTOR, '[class="ui-minute-picker"]'
            )
        time.sleep(1)

        filter_btn = browser.find_element(
            By.CSS_SELECTOR,
            '[class="btn btn-lg btn-block search-calendar"]',
        )

        filter_btn.click()
        time.sleep(10)

        first_result_date = browser.find_element(
            By.CSS_SELECTOR, '[class="event-block-date"]'
        ).text
        first_result_time = first_result_date.split()[1]
        print(first_result_time, filter_time)

    ##comment out from this line
    if first_result_time != filter_time:
        h_decrease_btn = time_input_h.find_element(
            By.CSS_SELECTOR, '[class="pi pi-chevron-down"]'
        ).click()
        print("i decreased the hour")
        filter_btn = browser.find_element(
            By.CSS_SELECTOR,
            '[class="btn btn-lg btn-block search-calendar"]',
        ).click()
        time.sleep(7)
        first_result_date = browser.find_element(
            By.CSS_SELECTOR, '[class="event-block-date"]'
        ).text
        first_result_time = first_result_date.split()[1]
        print(first_result_time, filter_time)
    if first_result_time != filter_time:
        h_increase_btn = time_input_h.find_element(
            By.CSS_SELECTOR, '[class="pi pi-chevron-up"]'
        )
        h_increase_btn.click()
        h_increase_btn.click()
        print("i increased the hour")
        filter_btn = browser.find_element(
            By.CSS_SELECTOR,
            '[class="btn btn-lg btn-block search-calendar"]',
        ).click()
        time.sleep(7)

        # if the date still does not match, reduce the day in the calender by 1
        first_result_date = browser.find_element(
            By.CSS_SELECTOR, '[class="event-block-date"]'
        ).text
        first_result_time = first_result_date.split()[1]
        if first_result_time != filter_time:
            available_days = browser.find_elements(By.CSS_SELECTOR, ".ui-state-default")
            for day in available_days:
                if int(day.text.strip()) == int(day_to_search) - 1:
                    day.click()
                    break
            #     m_increase_btn = time_input_m.find_element(
            #         By.CSS_SELECTOR, '[class="pi pi-chevron-up"]'
            #     ).click()
            filter_btn = browser.find_element(
                By.CSS_SELECTOR,
                '[class="btn btn-lg btn-block search-calendar"]',
            ).click()
            time.sleep(7)


def get_last_league_date():
    from datetime import datetime
    import calendar

    with open("data/data_dv_sam.txt", "r") as file:
        txt_file = file.readlines()
    date_time = txt_file[-2].strip().split()
    date, time_24h = date_time[0], date_time[1]

    return [date, time_24h]


class MyCustomThread(threading.Thread):
    # def __init__(self, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: codecs.Iterable[codecs.Any] = ..., kwargs: threading.Mapping[str, codecs.Any] | None = None, *, daemon: bool | None = None) -> None:
    #     super().__init__(group, target, name, args, kwargs, daemon=daemon)
    def __init__(
        self,
        group=None,
        target=None,
        name=None,
        args=(),
        kwargs={},
        Verbose=None,
        daemon=bool,
    ):
        threading.Thread.__init__(
            self, group, target, name, args, kwargs, daemon=daemon
        )
        self._return = None

    def run(self):
        self.error = None
        if self._target is not None:
            try:
                self._return = self._target(*self._args, **self._kwargs)
            except BaseException as e:
                self.error = e

    # def check_error(self):
    #     if self.exc:
    #         raise self.exc

    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return
