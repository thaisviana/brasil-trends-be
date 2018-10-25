from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchWindowException
import os
from elections.service import ElectionService
from time import sleep

qs = ['/m/0dsyzf', '/g/11b7r5bgrp', '/g/12215271', '/g/11g65h1pms', '/m/0bcdmp', '/m/0h_sx', '/g/11gb3ncsl_',
      '/m/04gc4vp', '/g/120wl4mm', '/m/05ghl4', '/m/047dbx9', '/m/04g5q20', '/m/0b4fnb', '/m/0pc9q']


class Command(BaseCommand):
    help = 'get keywords for candidates'

    def enable_headless_download(self, browser, download_path):
        # Add missing support for chrome "send_command"  to selenium webdriver
        browser.command_executor._commands["send_command"] = \
            ("POST", '/session/$sessionId/chromium/send_command')

        params = {'cmd': 'Page.setDownloadBehavior',
                  'params': {'behavior': 'allow', 'downloadPath': download_path}}
        browser.execute("send_command", params)

    def download_csvs(self):
        url = 'https://thaisnviana:@trends.google.com/trends/explore?date=now%207-d&geo=BR&q='
        from urllib.request import pathname2url
        import webbrowser, os
        # driver_location = '/Users/thaisviana/Downloads/chromedriver'
        # # The directory that you want to save the CSV to
        # download_path = './data'
        #
        # # Tell Selenium where to save downloaded files
        # chrome_options = Options()
        # download_prefs = {'download.default_directory': download_path,
        #                   'download.prompt_for_download': False,
        #                   'profile.default_content_settings.popups': 0}
        # chrome_options.add_experimental_option('prefs', download_prefs)
        #
        # # Tell Selenium to operate without a browser window
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--window-size=1920x1080')

        for q in qs:
            #url = 'file:{}'.format(pathname2url(os.path.abspath(path+q)))
            webbrowser.open(url+q)
            pass
            # driver = webdriver.Chrome(executable_path=driver_location, chrome_options=chrome_options)
            #
            # # Use the hack above to enable headless download
            # Command.enable_headless_download(None, driver, driver_location)
            # try:
            #     driver.get(url + q)
            #     print(driver.title)
            #     elem = driver.find_elements_by_xpath("//button[@class='widget-actions-item export']")
            #     for e in elem:
            #         e.click()
            #     driver.close()
            #     sleep(20)
            # except NoSuchWindowException as error:
            #     print(str(error.msg))


    def save_csv(self):
        for file in os.listdir('/Users/thaisviana/Desktop/'):
            if '.csv' in file:
                arq = open('/Users/thaisviana/Desktop/' + file, 'r')
                row_0 = arq[0]
                name = row_0
                name = name.split(':')[0]
                c = ElectionService.get_candidate_by_name(name)
                if c:
                    for line in arq[1:]:
                        ElectionService.process_and_save_word(c, line.mes, line.size_mes, 'now 1-7')

    def handle(self, *args, **options):
        self.download_csvs()