import requests
import datetime
import time

class LeetCodePlatform:
    API_URL = "https://leetcode.cn/graphql/noj-go/"
    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "content-type": "application/json"
    }

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
        resp = requests.post(self.API_URL, headers=self.HEADERS, json=payload)
        data = resp.json()
        ac_list = data.get("data", {}).get("recentACSubmissions", [])
        # 计算date当天的时间戳范围
        start_ts = int(time.mktime(date.timetuple()))
        end_ts = int(time.mktime((date + datetime.timedelta(days=1)).timetuple()))
        # 统计当天通过的题目（去重）
        titles = set()
        for ac in ac_list:
            ts = ac["submitTime"]
            if start_ts <= ts < end_ts:
                titles.add(ac["question"]["titleSlug"])
        return len(titles)

