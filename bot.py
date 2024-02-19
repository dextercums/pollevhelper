import os
import logging
import time
import json
import random
from playwright.sync_api import sync_playwright

logger = logging.getLogger('dexterbot')
__all__ = ['DexterBot']

class DexterBot:
    def __init__(self, user: str, password: str, host: str,
                 login_type: str = 'berkeley', lifetime: float = 60 * 60 * 2):
        if login_type not in {'berkeley'}:
            raise ValueError(f"'{login_type}' is not a supported login type. ")

        self.user = user
        self.password = password
        self.host = host
        self.login_type = login_type

        self.lifetime = lifetime
        self.start_time = time.time()

        self.browser = None
        self.page = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        return self
    
    def __exit__(self, *args):
        self.browser.close()
        self.playwright.stop()
    
    @staticmethod
    def timestamp() -> float:
        return round(time.time() * 1000)
    
    def save_session_state(self, cookies_file='cookies.json'):
        with open(cookies_file, 'w') as file:
            cookies = self.page.context.cookies()
            json.dump(cookies, file)

    def load_session_state(self, cookies_file='cookies.json'):
        if os.path.exists(cookies_file):
            with open(cookies_file, 'r') as file:
                cookies = json.load(file)
                self.page.context.add_cookies(cookies)
            return True
        else:
            logger.info("Cookies file does not exist.")
            return False
    
    def get_berkeley_cookies(self):
        self.page.goto('https://pollev.com/login?redirect=https%3A%2F%2Fpollev.com%2F' + self.host)
        self.page.wait_for_timeout(500) 
        self.page.fill('input[name="username"]', 'TOPDOG@berkeley.edu')
        self.page.wait_for_timeout(500) 
        self.page.click('.mdc-button')
        self.page.wait_for_timeout(500) 
        self.page.click('.mdc-button')
        self.page.wait_for_timeout(500) 

        self.page.fill('input[name="username"]', self.user)
        self.page.fill('input[name="password"]', self.password)
        self.page.wait_for_timeout(500) 
        self.page.click('#submit')

        logger.info("Login successful.")

        # wait for 2FA 
        self.page.wait_for_selector('#trust-browser-button')
        self.page.click('#trust-browser-button') 

        # wait for the login shit to go through
        self.page.wait_for_timeout(10000)

        self.save_session_state('cookies.json')

        logger.info("Cookies saved.")

    def get_login_cookies(self):
        self.get_berkeley_cookies()

    def login(self):
        # need to login
        if not self.load_session_state():
            self.get_login_cookies()

        self.page.goto('https://pollev.com/' + self.host)
        self.page.wait_for_timeout(2000)

        # cookies need refresh
        if self.page.is_visible('text="Pre-registration required"'):
            logger.info('Cookies out of date. Re-logging in')
            self.get_login_cookies()
            self.page.goto('https://pollev.com/' + self.host)
            self.page.wait_for_timeout(2000)

        if self.page.is_visible('text="Poll Everywhere helps boost engagement during remote meetings, virtual trainings, and online conferences."'):
            logger.info('Waiting for class to start')
        # <div class="component-response-header__status" aria-live="polite"><span></span>This poll is locked.</div>
        elif self.page.is_visible('text=This poll is locked.'):
            logger.info('Missed a poll you LATE FUCK')
        else:
            logger.info('Could not login')
    
    def answer_in_loop(self):
        count = 0
        polls_answered = 0
        while self.alive():
            buttons = self.page.locator('.component-response-multiple-choice__option__vote')
            if buttons.count() > 0 and not buttons.first.is_disabled():
                buttons.first.click()
                polls_answered += 1
                logger.info(f'Poll Answered: {polls_answered}')
            logger.info('Open Poll not found, checking again in 20 seconds')
            time.sleep(20)
            count += 1
            if count == 3: 
                time.sleep(random.randint(0,5)) 
                logger.info('Reloading page.')
                self.page.goto('https://pollev.com/' + self.host)
                count = 0
        logger.info('Bot lifetime over!')

    def alive(self):
        return time.time() <= self.start_time + self.lifetime

    def run(self):
        self.login()
        self.answer_in_loop()
        
