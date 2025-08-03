from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tools import get_teams_scores, print_both, filter_history
from selenium.webdriver.common.keys import Keys
import time


class ScrapeHistoryData:
    def __init__(self, driver: object,) -> None:
        self.browser = driver
        self.wait = WebDriverWait(driver=self.browser, timeout=10)

    def checkout_virtual(self, league: str):
        # show_more_btn = self.browser.find_element(
        #     By.CSS_SELECTOR, '[class="icon-down-default"]')
        show_more_btn = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[class="icon-down-default"]')))

        show_more_btn.click()
        time.sleep(1)
        available_leagues = self.browser.find_elements(
            By.CSS_SELECTOR, '[class="grid-left playlist-description"]')
        for league_btn in available_leagues:
            try:
                if league_btn.text == league.title():
                    league_btn.click()
                    time.sleep(2)
                    break
            except:
                pass

    def get_teams_and_scores(self, filter_date=None, filter_time=None):
        history_btn = self.browser.find_element(
            By.CSS_SELECTOR, '[class="result-history-title text--uppercase"]')
        history_btn.click()
        time.sleep(20)

        filter_history(self.browser, filter_date, filter_time)

        full_results_history = {}
        for _ in range(31):
            result = get_teams_scores(
                self.browser, full_results_history)
            full_results_history, date = result[0], result[1]
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            back_btn = self.browser.find_element(
                By.CSS_SELECTOR, '[class="icon icon-1_8x icon-left ng-star-inserted"]')
            back_btn.click()
            time.sleep(20)
            # scroll using keyboard
            body = self.browser.find_element(By.TAG_NAME, 'body')
            # body.send_keys(Keys.PAGE_DOWN)  # Scroll down
            body.send_keys(Keys.PAGE_UP)    # Scroll up
            time.sleep(1)
        # print_both(full_results_history)
        # print_both(f"\nlast date checked: {date}\n")
