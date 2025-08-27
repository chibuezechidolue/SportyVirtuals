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


def get_team_scores(
    browser,
):
    events = browser.find_elements(
        By.CSS_SELECTOR, '[class="history-container ng-star-inserted"]'
    )
    current_result = {}
    for event in events:
        week = event.find_element(
            By.CSS_SELECTOR, '[class="event-block-id ng-star-inserted"]'
        ).text
        # date = event.find_element(By.CSS_SELECTOR, '[class="event-block-date"]').text
        print(week)
        # if week == "Week 34":
        #     pass
        current_result[week] = {}
        week_result = event.find_element(By.CSS_SELECTOR, '[class="panel-body"]')

        for n in range(4):
            matches_in_week_result = week_result.find_elements(
                By.CSS_SELECTOR, '[class="ng-star-inserted"]'
            )[n * 5 :]
            for match in matches_in_week_result:
                h_team = match.find_element(
                    By.CSS_SELECTOR, '[class="teamA flex-col"]'
                ).text
                a_team = match.find_element(
                    By.CSS_SELECTOR, '[class="teamB flex-col"]'
                ).text
                # score = match.find_element(By.CSS_SELECTOR, '[class="flex-col match-result-score p-1"').text
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
                    By.CSS_SELECTOR,
                    '[class="flex-row p-1 won-markets ng-star-inserted"]',
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
                        ht_ft = (ht_ft_outcome[0].strip(),)
                    elif outcome.text.strip() == "CORRECT SCORE":
                        next_sibiling = outcome.find_element(
                            By.XPATH, "following-sibling::*[1]"
                        )
                        cs_outcome = next_sibiling.text.split(":")
                        cs = cs_outcome[0].strip()
                        break

                current_result[week][f"{h_team} - {a_team}"] = {
                    "correct_score": [cs],
                    "ht/ft": [ht_ft],
                }

                match.click()

                load_more_btn = browser.find_element(
                    By.CSS_SELECTOR,
                    '[class="btn-load-more-tickets btn btn-lg btn-block ng-star-inserted"]',
                )
                load_more_btn.click()
                time.sleep(5)

    return current_result


def print_both(*args):
    """To print on the terminal as well as an output file"""
    with open("new.txt", "at") as file:
        to_print = " ".join([str(arg) for arg in args])
        # print(to_print)
        print(to_print, file=file)
        # file.write(to_print)


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
