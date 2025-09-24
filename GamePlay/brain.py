import time
import os
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException,
)
from tools import clear_betslip, find_week_to_play, get_team_scores

from dotenv import load_dotenv

load_dotenv()


class PlayGame:
    """To handle the Game Play like: choose_market, select_stake_option,
    place_the_bet. It takes a driver instance as first argument"""

    def __init__(
        self,
        driver: object,
    ) -> None:
        self.browser = driver
        self.wait = WebDriverWait(driver=self.browser, timeout=10)

    def choose_league(self, league: str):
        """To select the market which was passed as a variable during initializing"""
        ftball_leagues = self.wait.until(
            EC.element_to_be_clickable((By.ID, "game_league"))
        )

        ftball_leagues.click()
        time.sleep(1)
        selected_league = self.browser.find_element(
            By.CSS_SELECTOR, '[title="Germany"]'
        )
        selected_league.click()
        time.sleep(10)

    def select_stake_options(self, week: str, pattern_types: dict) -> str:
        """To select the stake option from the selected market, you wish to stake funds on"""
        for market, stake in pattern_types.items():
            if market == "ht/ft":
                market = "Others"
            market_option = self.browser.find_element(
                By.CSS_SELECTOR, f'[title="{market}"]'
            )
            try:
                market_option.click()
            except ElementClickInterceptedException:
                # print("An ElementClickInterceptedException occured")
                self.browser.execute_script(
                    'arguments[0].scrollIntoView({block: "center", inline: "center"});',
                    market_option,
                )
                market_option.click()

            available_weeks = self.browser.find_elements(
                By.CSS_SELECTOR,
                ".panel.mb-2.ng-trigger.ng-trigger-collapseVerticalOut.market.open.ng-star-inserted",
            )

            week_to_play = find_week_to_play(week, available_weeks)
            available_stakes = week_to_play.find_elements(
                By.CSS_SELECTOR,
                '[class="grid grid-middle grid-center odd-name gr-col-12 ng-star-inserted"]',
            )
            for option in available_stakes:
                if option.text == stake:
                    try:
                        option.click()
                    except ElementClickInterceptedException:
                        self.browser.execute_script(
                            'arguments[0].scrollIntoView({block: "center", inline: "center"});',
                            option,
                        )
                        option.click()

            time.sleep(1)
        return week

    def place_the_bet(self, amount: int, test: bool) -> str:
        """To bet the selected stake options each with the inputed amount"""
        singles_input = self.browser.find_element(
            By.CSS_SELECTOR, "#bets-stake-amount-1"
        )
        singles_input.send_keys(amount)
        if test:
            clear_betslip(self.browser)
        else:
            place_bet_btn = self.browser.find_element(
                By.CSS_SELECTOR, '[class="bet-now btn btn-lg btn-block"]'
            )
            place_bet_btn.click()


class CheckPattern:
    """To check if the the desired pattern of the desired market has occured.
    It takes a driver instance as first argument"""

    def __init__(self, driver: object, market: str) -> None:
        self.market = market
        self._VIRTUAL_BUTTON_LINK_TEXT = "VIRTUAL"
        self.browser = driver
        self.wait = WebDriverWait(driver=self.browser, timeout=10)

    def checkout_virtual(self, league: str):
        """To enter the desired Virtual Game option(e.g. Bundesliga)"""

    def check_result(
        self,
        league: str,
        weeks_to_check: int,
        acc_balance: str = None,
        to_play: int = None,
    ) -> dict:
        """To check the result outcomes of an inputed length or number of weeks"""

        ftball_leagues = self.wait.until(
            EC.element_to_be_clickable((By.ID, "game_league"))
        )

        ftball_leagues.click()
        time.sleep(1)
        league_result_btn = ftball_leagues.find_element(
            By.ID, "game_league_results-history"
        )
        league_result_btn.click()
        time.sleep(5)
        result_league_menu = self.browser.find_element(
            By.CSS_SELECTOR, '[class="menu"]'
        )
        available_leagues = result_league_menu.find_elements(By.TAG_NAME, "div")
        for league_btn in available_leagues:
            try:
                if league_btn.text.strip() == league.title():
                    league_btn.click()
                    time.sleep(1)
                    break
            except:
                pass
        time.sleep(5)
        last_result = get_team_scores(self.browser, weeks_to_check)
        return last_result

    def check_for_pattern(self, league, weeks_to_check, pattern_type):
        result = self.check_result(league, weeks_to_check)
        for week, outcome in result.items():
            response = ""
            for team, results in outcome.items():
                correct_score = results["correct_score"]
                ht_ft = results["ht/ft"]
                if pattern_type == "ht/ft":
                    if ht_ft == "2/1" or ht_ft == "1/2":
                        return {"ht/ft": "2/1", "ht/ft": "1/2"}
                elif pattern_type == "3-3 or 1/2 or 2/1":
                    if correct_score == "3-3" or ht_ft == "1/2":
                        return {"Correct Score": "3-3", "ht/ft": "1/2"}
                    elif correct_score == "3-3" or ht_ft == "2/1":
                        return {"correct_score": "3-3", "ht/ft": "2/1"}
                elif pattern_type == "4-0 or 0-4":
                    if correct_score == "4-0" or correct_score == "0-4":
                        return {"correct_score": "4-0", "correct_score": "0-4"}
                else:
                    response = "No Pattern Found"
        return response


class User:
    """To login a user with the relevant credentials.
    It takes a driver instance as first argument"""

    def __init__(self, driver: object, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.browser = driver
        self.wait = WebDriverWait(driver=self.browser, timeout=10)

    def login(self):
        """Login the user with the credentialsfrom initialization and return the account balance of the user"""
        self.browser.switch_to.default_content()
        login_btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="logIn"]'))
        )
        login_btn.click()
        time.sleep(2)

        user_input = self.browser.find_element(By.CSS_SELECTOR, '[name="phone"]')
        password_input = self.browser.find_element(By.CSS_SELECTOR, '[type="password"]')

        for char in self.username:
            time.sleep(0.5)
            user_input.send_keys(char)
        for char in self.password:
            time.sleep(0.5)
            password_input.send_keys(char)
        time.sleep(1)

        try:
            login_button = self.browser.find_element(
                By.CSS_SELECTOR, '[class="af-button af-button--primary"]'
            )
            login_button.click()
        except:
            login_button = self.browser.find_element(
                By.CSS_SELECTOR, '[class="m-btn m-btn-login"]'
            )
            login_button.click()
        time.sleep(2)

        acc_balance = (
            self.browser.find_element(By.CSS_SELECTOR, '[id="j_balance"]').text.strip()
            # .split()[0]
        )
        print(acc_balance.split()[0])
        iframe = self.browser.find_element(By.TAG_NAME, "iframe")
        self.browser.switch_to.frame(iframe)
        return acc_balance.split()[0]
