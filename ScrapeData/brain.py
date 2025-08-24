from zoneinfo import available_timezones
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
        ftball_leagues = self.wait.until(EC.element_to_be_clickable(
            (By.ID, "game_league")))

        ftball_leagues.click()
        time.sleep(1)
        league_result_btn = ftball_leagues.find_element(
            By.ID, "game_league_results-history")
        league_result_btn.click()
        time.sleep(1)
        result_league_menu = ftball_leagues.find_element(
            By.CSS_SELECTOR, '[class="menu"]')
        available_leagues = result_league_menu.find_elements(
            By.TAG_NAME, "div")
        for league_btn in available_leagues:
            try:
                if league_btn.text.strip() == league.title():
                    league_btn.click()
                    time.sleep(2)
                    break
            except:
                pass

    def get_teams_and_scores(self, filter_date=None, filter_time=None):

        # filter_history(self.browser, filter_date, filter_time)

        full_results_history = {}
        for _ in range(31):
            result = get_teams_scores(
                self.browser, full_results_history)
            full_results_history, date = result[0], result[1]
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            load_more_btn = self.browser.find_element(
                By.CSS_SELECTOR, '[class="icon icon-1_8x icon-left ng-star-inserted"]')
            load_more_btn.click()
            time.sleep(20)
            # scroll using keyboard
            body = self.browser.find_element(By.TAG_NAME, 'body')
            # body.send_keys(Keys.PAGE_DOWN)  # Scroll down
            body.send_keys(Keys.PAGE_UP)    # Scroll up
            time.sleep(1)

        # print_both(full_results_history)
        # print_both(f"\nlast date checked: {date}\n")
