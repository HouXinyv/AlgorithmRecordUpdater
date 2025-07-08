import requests
import datetime
import time
from platforms.base import BasePlatform
import pytz

class VJudgePlatform(BasePlatform):
    def __init__(self):
        """
        VJudge平台实现
        """
        super().__init__("VJudge")

    def get_ac_count(self, user_id: str, date: datetime.date) -> int:
        """
        获取指定用户在指定日期的AC题目数量
        :param user_id: vjudge用户名
        :param date: 日期对象
        :return: 通过题目数量
        """
        params = {
            "draw": 9,
            "start": 0,
            "length": 20,  # Adjust length to fetch more submissions if needed
            "un": user_id,
            "OJId": "",
            "probNum": "",
            "res": 1,  # 1 for Accepted submissions
            "language": "",
            "onlyFollowee": "false",
            "orderBy": "run_id",
            "_": int(time.time() * 1000)  # Current timestamp in milliseconds
        }

        resp = requests.get(self.url, headers=self.headers, params=params)
        # 若响应异常，打印响应内容
        if resp.status_code != 200:
            print("响应状态码:", resp.status_code)
            print("响应内容:", resp.text)
            return 0

        data = resp.json()
        submissions = data.get("data", [])

        # 使用基类方法获取时间戳（注意：VJudge使用毫秒时间戳）
        start_ts = self.get_start_timestamp(date) * 1000
        end_ts = self.get_end_timestamp(date) * 1000

        # Count unique accepted problems on the specified date
        prob_nums = set()
        for submission in submissions:
            if submission.get("status") == "Accepted":
                ts = submission.get("time", 0)
                if start_ts <= ts < end_ts:
                    prob_nums.add(submission["probNum"])

        return len(prob_nums)

if __name__ == "__main__":
    # Test the VJudgePlatform class
    platform = VJudgePlatform()
    test_user = "bucuo"
    test_date = datetime.date(2025, 5, 27)  # Example date based on provided data
    ac_count = platform.get_ac_count(test_user, test_date)
    print(f"{test_user} solved {ac_count} problems on {test_date}")