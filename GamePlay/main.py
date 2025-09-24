import os
import time
from selenium.webdriver.common.by import By
from tools import reduce_week_selected, set_up_driver_instance, MyCustomThread
from datetime import datetime
from dotenv import load_dotenv
from brain import CheckPattern, User, PlayGame

load_dotenv()

SELECTED_MARKET = "ht/ft"
LEAGUE = "germany"
PATTERN = "3-3 or 1/2 or 2/1"  # "ht/ft"
AMOUNT_LIST = (
    10,
    10,
    10,
    20,
    30,
    40,
    55,
    80,
    110,
    160,
    230,
    330,
    470,
    675,
    970,
    1390,
    1980,
    2840,
    4050,
    5800,
    8300,
    11850,
    16950,
    24250,
)
MAX_AMOUNT_LENGTH = 14
TOTAL_AMOUNT = 450000


def run_game_play():
    # browser=webdriver.Chrome()           # driver instance with User Interface (not headless)
    browser = (
        set_up_driver_instance()
    )  # driver instance without User Interface (--headless)
    browser.get("https://www.sportybet.com/ng/virtual/")
    time.sleep(20)
    # switch to bet activities frame

    iframe = browser.find_element(By.TAG_NAME, "iframe")
    browser.switch_to.frame(iframe)
    user = User(
        browser,
        os.environ.get("SPORTY_USERNAME"),
        os.environ.get("SPORTY_PASSWORD"),
    )
    acc_bal = user.login()
    ijhskjhjk
    print("i have lunched")
    # pattern = CheckPattern(browser, market=SELECTED_MARKET)
    # response = pattern.check_for_pattern(
    #     league=LEAGUE, weeks_to_check=10, pattern_type=PATTERN
    # )
    # print(response)
    response = {"Correct Score": "3-3", "ht/ft": "1/2"}

    play = PlayGame(driver=browser)
    play.choose_league(league=LEAGUE)
    if response != "No Pattern Found":
        user = User(
            browser,
            os.environ.get("SPORTY_USERNAME"),
            os.environ.get("SPORTY_PASSWORD"),
        )
        acc_bal = user.login()
        # acc_bal = float(acc_bal.replace(",", "_"))
        GAME_LEVEL = round((acc_bal - 1000) / TOTAL_AMOUNT, 2)
        time.sleep(1)
        for n in range(len(AMOUNT_LIST[:MAX_AMOUNT_LENGTH])):
            week_selected = play.select_stake_options(
                week="Week 21",
                pattern_types=response,
            )
            acc_bal = play.place_the_bet(
                amount=str(AMOUNT_LIST[n] * GAME_LEVEL),
                test=eval(os.environ.get("TEST")),
            )

            # reduce_week_selected(week_selected, by=0, league=LEAGUE)

            pattern = CheckPattern(browser, market=SELECTED_MARKET)
            pattern.check_for_pattern(LEAGUE, weeks_to_check=1, pattern_type=PATTERN)
            # N.B: pattern_type needs to be dynamic, not a static name variable above


run_game_play()
