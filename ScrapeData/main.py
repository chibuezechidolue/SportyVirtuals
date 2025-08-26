import os
import time
from selenium.webdriver.common.by import By
from tools import set_up_driver_instance, get_last_league_date, MyCustomThread
from brain import ScrapeHistoryData
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def run_data_collection():
    date_time = get_last_league_date()

    # DATE,TIME="06/29","17:15"
    DATE, TIME = date_time[0], date_time[1]
    # DATE, TIME = None, None
    print(DATE, TIME)
    if os.environ.get("OPERATING_SYSTEM") == "windows":
        # Windows OS: to kill all process with the given process_name
        os.system(f"taskkill /f /t /im chrome.exe")
    elif os.environ.get("OPERATING_SYSTEM") == "linux":
        # Linux OS: to kill all process with the given process_name
        os.system(f"killall chrome")

    browser = set_up_driver_instance()

    # visit sportbet scheduled virtuals
    # url = "https://virtual-games.virtustec.com/mobile-v4/?v=2.8.2&hwId=49690d2f-0517-46ff-bd66-6aedd9958826&showHeader=true&showFooter=true&showMenuBetHistory=false&showMenuProfile=false&showMenuCredit=false&showMenuLoginButton=false&showMenuLogoutButton=false"
    url = "https://www.sportybet.com/ng/virtual/"
    browser.get(url)
    time.sleep(30)
    # switch to bet activities frame
    iframe = browser.find_element(By.TAG_NAME, "iframe")
    browser.switch_to.frame(iframe)

    scrape = ScrapeHistoryData(driver=browser)
    scrape.checkout_virtual(league="germany")
    time.sleep(5)
    scrape.get_teams_and_scores(DATE, TIME)
    print("I am done!!!")


run_data_collection()
djhhj
if __name__ == "__main__":
    while True:
        if os.environ.get("OPERATING_SYSTEM") == "windows":
            # Windows OS: to kill all process with the given process_name
            os.system(f"taskkill /f /t /im chrome.exe")
        elif os.environ.get("OPERATING_SYSTEM") == "linux":
            # Linux OS: to kill all process with the given process_name
            os.system(f"killall chrome")

        # bot=mp.Process(target=play_bot,daemon=True)
        bot = MyCustomThread(target=run_data_collection, daemon=True)
        bot.start()
        bot.join()
        if bot.error:
            print(bot.error)
        # bot.terminate()
        print("bot terminated")
