import requests
import datetime
import time

from platforms.base import BasePlatform


class LeetCodePlatform(BasePlatform):
    def __init__(self):
        super().__init__("LeetCode")

    def get_ac_count(self, user_id: str, date: datetime.date) -> int:
        """
        获取指定用户在指定日期的AC题目数量
        :param user_id: leetcode用户名
        :param date: 日期对象
        :return: 通过题目数量
        """
        query = '''
        query recentAcSubmissions($userSlug: String!) {
          recentACSubmissions(userSlug: $userSlug) {
            submissionId
            submitTime
            question {
              title
              translatedTitle
              titleSlug
              questionFrontendId
            }
          }
        }
        '''
        variables = {"userSlug": user_id}
        payload = {
            "query": query,
            "variables": variables,
            "operationName": "recentAcSubmissions"
        }
        resp = requests.post(self.url, headers=self.headers, json=payload)
        data = resp.json()
        ac_list = data.get("data", {}).get("recentACSubmissions", [])
        # 计算date当天的时间戳范围

        # 使用基类方法获取时间戳
        start_ts = self.get_start_timestamp(date)
        end_ts = self.get_end_timestamp(date)

        # 统计当天通过的题目（去重）
        titles = set()
        for ac in ac_list:
            ts = ac["submitTime"]
            if start_ts <= ts < end_ts:
                titles.add(ac["question"]["titleSlug"])
        return len(titles)


if __name__ == "__main__":
    # 测试 miao-bao-kh-khmiao-cai-cai 用户
    platform = LeetCodePlatform()
    import datetime

    test_user = "holden_sn"
    test_date = datetime.date(2025, 7, 7)  # 可替换为任意日期
    count = platform.get_ac_count(test_user, test_date)
    print(f"{test_user} 在 {test_date} 的LeetCode做题数: {count}")
