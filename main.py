from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

PROMISED = 150
EMAIL = os.environ.get("email")
PASSWORD = os.environ.get("pass")
USERNAME = os.environ.get("username")


class InternetSpeedTwitterBot:
    def __init__(self):
        self.up = None
        self.down = None
        self.driver = webdriver.Firefox()

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        time.sleep(6)
        self.driver.find_element(By.CLASS_NAME, "start-text").click()
        time.sleep(50)
        self.down = float(self.driver.find_element(By.CLASS_NAME, "download-speed").text)
        self.up = float(self.driver.find_element(By.CLASS_NAME, "upload-speed").text)
        return {"down": self.down, "up": self.up}

    def tweet_at_provider(self, text):
        self.driver.get("https://twitter.com/")
        time.sleep(6)
        self.driver.find_element(By.LINK_TEXT, "Log in").click()
        time.sleep(3)
        user = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
        user.send_keys(USERNAME)
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div').click()
        time.sleep(3)
        user_pass = self.driver.switch_to.active_element
        user_pass.send_keys(PASSWORD)
        user_pass.send_keys(Keys.ENTER)
        time.sleep(6)
        self.driver.find_element(By.CSS_SELECTOR, '.public-DraftStyleDefault-block').click()
        input_box = self.driver.switch_to.active_element
        input_box.send_keys(text)
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div').click()


tweet_bot = InternetSpeedTwitterBot()
speed = tweet_bot.get_internet_speed()
print(speed)
if speed["down"] < PROMISED or speed["up"] < PROMISED:
    text = f" Promised speed DOWN: {PROMISED}Mbps, UP: {PROMISED}Mbps, but currently my speed is Down: {speed['down']}Mbps, Up: {speed['up']}Mbps"
    tweet_bot.tweet_at_provider(text)
