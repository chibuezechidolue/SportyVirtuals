from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (StaleElementReferenceException, NoSuchElementException,
                                        TimeoutException, ElementClickInterceptedException)
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

import time
import threading
import os
import psutil


def set_up_driver_instance():
    """ To create and return a webdriver object with disabled gpu and headless"""

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'

    chrome_options = webdriver.ChromeOptions()  # Google Chrome
    # chrome_options = webdriver.EdgeOptions()      # Microsoft Edge
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")

    # to stop printing error messages to the console
    chrome_options.add_argument('--log-level=3')
    # chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--disable-application-cache')
    chrome_options.add_argument('--disable-extensions')

    # prefs={'profile.default_content_setting_values': {'images': 2, 'javascript': 2}}
    # prefs = {"profile.managed_default_content_settings.images": 2, "profile.default_content_setting_values.javascript": 2}
    prefs = {'profile.default_content_setting_values': {'images': 2, "stylesheet": 2,
                                                        'plugins': 2, 'popups': 2, 'geolocation': 2,
                                                        'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                                                        'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                        'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
                                                        'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                        'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
                                                        'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
                                                        'durable_storage': 2}}
    chrome_options.add_experimental_option('prefs', prefs)

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
    return webdriver.Chrome(options=chrome_options)   # Google Chrome
    # return webdriver.Edge(options=chrome_options)       # Microsoft Edge


def get_teams_scores(browser, full_results_history: dict) -> dict:
    events = browser.find_elements(
        By.CSS_SELECTOR, '[class="eventBlock ng-star-inserted"]')
    # print("events: ", len(events))
    events[0].click()
    # full_results_history = {}
    for event in events:
        heading = event.find_element(
            By.CSS_SELECTOR, '[class="row col-xs-12 history__event-day"]')
        date = event.find_element(
            By.CSS_SELECTOR, '[class="row col-xs-12 history__event-time"]')
        league_id = heading.find_element(By.CSS_SELECTOR, 'span').text
        week = heading.text[len(league_id)+1:]
        if not league_id in full_results_history:
            if full_results_history != {}:
                print_both(full_results_history)
                # print_both(f"\n{date.text}\n\n")
                print_both(f"{date.text}\n")
            full_results_history = {}
            full_results_history[league_id] = {}
            print(league_id)
        full_results_history[league_id][week] = {}

        event.click()
        week_results = event.find_elements(
            By.CSS_SELECTOR, '.collapsable')
        for week_result in week_results:
            # week_scores = week_result.find_elements(
            #     By.CSS_SELECTOR, '[class="grid grid-middle title-center ng-star-inserted"]')
            matches_in_week_result = week_result.find_elements(
                By.CSS_SELECTOR, '[class="event ng-star-inserted"]')
            for match in matches_in_week_result:
                match.click()
                h2h_score = match.find_element(
                    By.CSS_SELECTOR, '[class="grid grid-middle title-center ng-star-inserted"]')
                h2h_score = h2h_score.text
                h_team, a_team = h2h_score[:3], h2h_score[-3:]
                score = h2h_score[3:-3].strip()
                won_content = match.find_element(
                    By.CSS_SELECTOR, '[class="col-xs-12 content"]')

                # To find the won outcome based on rows and colunmn a specific won outcome is located
                rows = won_content.find_elements(
                    By.CSS_SELECTOR, '[class="row ng-star-inserted"]')
                cs_ht_ft_row = rows[1]
                cols = cs_ht_ft_row.find_elements(
                    By.CSS_SELECTOR, '[class="col-xs-4 ng-star-inserted"]')

                cs_col = cols[0]
                cs = cs_col.find_element(
                    By.CSS_SELECTOR, '[class="odd-market text--uppercase"]').text.strip()
                cs_odd = cs_col.find_element(
                    By.CSS_SELECTOR, '[class="grid grid-middle grid-center odd ng-star-inserted"]').text.strip()

                ht_ft_col = cols[1]
                ht_ft = ht_ft_col.find_element(
                    By.CSS_SELECTOR, '[class="odd-market text--uppercase"]').text.strip()
                ht_ft_odd = ht_ft_col.find_element(
                    By.CSS_SELECTOR, '[class="grid grid-middle grid-center odd ng-star-inserted"]').text.strip()

                full_results_history[league_id][week][f"{h_team} - {a_team}"] = {
                    "correct_score": [cs, cs_odd], "ht/ft": [ht_ft, ht_ft_odd]}

                match.click()
            # for score in week_scores:
            #     h2h_score = score.text
            #     h_team, a_team = h2h_score[:3], h2h_score[-3:]
            #     # score = h2h_score[3:-3].strip()
            #     # full_results_history[league_id][week][f"{h_team} - {a_team}"] = score

            #     score.click()
            #     full_results_history[league_id][week][f"{h_team} - {a_team}"] = [
            #         [], []]
            #     full_results_history[league_id][week][f"{h_team} - {a_team}"] = {
            #         ""}
        event.click()
    return [full_results_history, date.text]


def print_both(*args):
    """To print on the terminal as well as an output file"""
    with open('data1.txt', 'at') as file:
        to_print = ' '.join([str(arg) for arg in args])
        # print(to_print)
        print(to_print, file=file)
        # file.write(to_print)


# print_both('""duhjndjbjcxhvbzxh')


def filter_history(browser, filter_date: str, filter_time: str):
    if filter_date != None:
        # filter function
        # Set the begining date for filter
        date_input = browser.find_element(
            By.CSS_SELECTOR, '[name="date"]')
        # min_date = date_input.get_attribute("min")
        date_input.send_keys(filter_date)  # min_date

        # Set the filter time
        time_input = browser.find_element(
            By.CSS_SELECTOR, '[name="time"]')
        time_input.send_keys(filter_time)  # "12:00 AM"

        submit_btn = browser.find_element(
            By.CSS_SELECTOR, '[class="col-xs-12 valign-middle button ok-button text--uppercase"]')

        browser.execute_script("window.scrollTo(0, document.body.scrollTop);")
        # self.browser.execute_script(
        #     "return arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(10)
        submit_btn.click()
        time.sleep(10)
    else:
        # browser.execute_script("window.scrollTo(0, 0);")

        # scroll using keyboard
        body = browser.find_element(By.TAG_NAME, 'body')
        # body.send_keys(Keys.PAGE_DOWN)  # Scroll down
        body.send_keys(Keys.PAGE_UP)    # Scroll up
        time.sleep(1)


def get_last_league_date():
    from datetime import datetime
    with open("data1.txt", "r") as file:
        txt_file = file.readlines()
    date_time = txt_file[-2].split()
    date, time_24h = date_time[0], date_time[1]
    # format str to 24h datetime object
    dt_object = datetime.strptime(time_24h, "%H:%M")
    # Format the datetime object into a 12-hour time string with AM/PM
    time_12h = dt_object.strftime("%I:%M %p")
    date_split = date.split("/")
    new_date = f"{date_split[1]}/{date_split[0]}/{date_split[2]}"
    time_str = time_12h.replace(":", "").replace(" ", "")
    return [new_date, time_str]


class MyCustomThread(threading.Thread):
    # def __init__(self, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: codecs.Iterable[codecs.Any] = ..., kwargs: threading.Mapping[str, codecs.Any] | None = None, *, daemon: bool | None = None) -> None:
    #     super().__init__(group, target, name, args, kwargs, daemon=daemon)
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None, daemon=bool):
        threading.Thread.__init__(
            self, group, target, name, args, kwargs, daemon=daemon)
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
