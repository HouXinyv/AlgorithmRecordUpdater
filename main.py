import time
import schedule
from platforms.leetcode import LeetCodePlatform
from doc_updater.tencent_doc import TencentDocUpdater
from util.util_fun import load_users, get_yesterday, update_sheet

CONFIG_PATH = "config/users.json"
DOC_URL = "https://do" # todo: 共享文档的URL，需替换为实际的腾讯文档链接

TENCENT_DOC_COOKIES = {
    #  todo: 腾讯文档cookies
}

def main():
    users = load_users(CONFIG_PATH)
    doc = TencentDocUpdater(DOC_URL, cookies=TENCENT_DOC_COOKIES)
    leetcode = LeetCodePlatform()

    def job():
        date = get_yesterday()
        update_sheet(doc, leetcode, users, date)
        print(f"已更新 {date} 的数据到腾讯文档。")

    print("腾讯文档已打开，等待定时任务...")

    schedule.every().day.at("03:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(max(60, schedule.idle_seconds()))

if __name__ == "__main__":
    main()
