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
from tools import get_team_scores

from dotenv import load_dotenv

load_dotenv()


class PlayGame:
    """To handle the Game Play like: choose_market, select_stake_option,
    place_the_bet. It takes a driver instance as first argument"""

    def __init__(self, driver: object, market: str) -> None:
        self.market = market.lower()
        self.browser = driver
        self.wait = WebDriverWait(driver=self.browser, timeout=10)

    def choose_market(self):
        """To select the market which was passed as a variable during initializing"""

    def select_stake_options(self, week: str, previous_week_selected: str) -> str:
        """To select the stake option from the selected market, you wish to stake funds on"""

    def place_the_bet(self, amount: int, test: bool) -> str:
        """To bet the selected stake options each with the inputed amount"""


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
        # length: str,
        # latest_week: str,
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
        last_result = get_team_scores(self.browser)
        return last_result

    def check_pattern(self):
        result = self.check_result(league="germany")
        for k,v in result.items():
            


class LoginUser:
    """To login a user with the relevant credentials.
    It takes a driver instance as first argument"""

    def __init__(self, driver: object, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.browser = driver
        self.wait = WebDriverWait(driver=self.browser, timeout=10)

    def login(self):
        """Login the user with the credentials from initialization and return the account balance of the user"""
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
            password_input(char)
        time.sleep(1)

        login_button = self.browser.find_element(
            By.CSS_SELECTOR, '[class="af-button af-button--primary"]'
        )
        login_button.click()
        time.sleep(2)

        # acc_balance = self.browser.find_element(
        #     By.CSS_SELECTOR, ".user-balance-container .amount"
        # ).text
        # return acc_balance
