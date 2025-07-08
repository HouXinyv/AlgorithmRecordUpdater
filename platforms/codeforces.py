import requests
import datetime


from platforms.base import BasePlatform


class CodeforcesPlatform(BasePlatform):
    def __init__(self):
        """
        Codeforces平台初始化
        """
        super().__init__("Codeforces")

    def get_ac_count(self, user_id: str, date: datetime.date) -> int:
        """
        获取指定用户在指定日期的AC题目数量
        :param user_id: Codeforces用户名 (handle)
        :param date: 日期对象
        :return: 通过的题目数量
        """
        params = {
            "handle": user_id,
            "from": 1,
            "count": 100  # 获取足够多的提交记录以覆盖一天
        }
        try:
            resp = requests.get(self.url, headers=self.headers, params=params)
            resp.raise_for_status()  # 对于错误状态码抛出异常
            data = resp.json()

            if data.get("status") != "OK":
                return 0

            submissions = data.get("result", [])

            # 使用基类方法获取时间戳
            start_ts = self.get_start_timestamp(date)
            end_ts = self.get_end_timestamp(date)

            # 统计唯一通过的题目
            problem_ids = set()
            for submission in submissions:
                if submission.get("verdict") == "OK":
                    ts = submission.get("creationTimeSeconds")
                    if start_ts <= ts < end_ts:
                        problem = submission.get("problem", {})
                        # 使用contestId和index组合作为唯一题目标识
                        problem_id = f"{problem.get('contestId', '')}_{problem.get('index', '')}"
                        problem_ids.add(problem_id)

            return len(problem_ids)
        except requests.RequestException:
            return 0  # 网络或API错误时返回0


if __name__ == "__main__":
    # 测试代码
    cf_platform = CodeforcesPlatform()
    user_handle = "tourist"  # 示例用户
    date = datetime.date(2025, 7, 6)  # 示例日期
    ac_count = cf_platform.get_ac_count(user_handle, date)
    print(f"{user_handle} 在 {date} 的AC题目数量: {ac_count}")
