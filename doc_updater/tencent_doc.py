from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time


class TencentDocUpdater:
    def __init__(self, doc_url, cookies=None):
        # todo: 更改为自己的浏览器驱动，以及登录过腾讯文档后的profile路径
        profile_path = "/home/hxy/snap/firefox/common/.mozilla/firefox/2njivqga.default"
        profile = FirefoxProfile(profile_path)
        options = Options()
        self.driver = webdriver.Firefox(
            firefox_profile=profile,
            options=options,
            executable_path="/snap/bin/geckodriver"
        )
        time.sleep(5)
        if len(self.driver.window_handles) > 1:
            for handle in self.driver.window_handles[1:]:
                self.driver.switch_to.window(handle)
                self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

        self.driver.get(doc_url)

        # 等待页面加载
        time.sleep(5)
        # 注入cookie
        if cookies:
            for k, v in cookies.items():
                self.driver.add_cookie({'name': k, 'value': v})
            self.driver.refresh()
            time.sleep(2)

    def set(self, cell: str, value):
        # 1. 定位到输入框，输入单元格编号
        bar = self.driver.find_element(By.CSS_SELECTOR, ".formula-bar .bar-label")
        bar.clear()
        bar.send_keys(cell)
        bar.send_keys(Keys.ENTER)
        time.sleep(1)
        # 2. 定位到内容编辑框，输入内容
        editor = self.driver.find_element(By.CSS_SELECTOR, "#alloy-simple-text-editor")
        editor.clear()
        editor.send_keys(str(value))
        editor.send_keys(Keys.ENTER)
        time.sleep(0.5)

    def save(self):
        # 仅保存文档（Ctrl+S），不退出
        actions = ActionChains(self.driver)
        actions.key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()
        time.sleep(1)

    def close(self):
        # 先保存文档（Ctrl+S）
        self.save()
        self.driver.quit()
