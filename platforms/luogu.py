import requests
import datetime
import math

from platforms.base import BasePlatform


class LuoguPlatform(BasePlatform):
    def __init__(self):
        """
        洛谷平台初始化
        """
        super().__init__("Luogu")

    def get_ac_count(self, user_id: str, date: datetime.date) -> int:
        """
        获取指定用户在指定日期的AC题目数量
        :param user_id: 洛谷用户ID
        :param date: 日期对象
        :return: 通过的题目数量
        """
        # 计算指定日期的时间戳范围
        # 使用基类方法获取时间戳
        start_ts = self.get_start_timestamp(date)
        end_ts = self.get_end_timestamp(date)

        # 统计唯一通过的题目
        problem_ids = set()
        page = 1

        # 构建完整URL
        url = f"{self.url}?user={user_id}&status=12&page={page}&_contentOnly=1"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()  # 对于错误状态码抛出异常
        data = resp.json()

        if data.get("code") != 200:
            return 0

        records = data.get("currentData", {}).get("records", {}).get("result", [])

        for record in records:
            submit_ts = record.get("submitTime", 0)
            if start_ts <= submit_ts < end_ts:
                problem_id = record.get("problem", {}).get("pid", "")
                problem_ids.add(problem_id)

        return len(problem_ids)


if __name__ == "__main__":
    """
    测试LuoguPlatform的get_ac_count方法
    """
    platform = LuoguPlatform()
    test_user_id = "992260"  # 示例用户ID
    test_date = datetime.date(2023, 4, 21)  # 示例日期
    ac_count = platform.get_ac_count(test_user_id, test_date)
    print(f"用户 {test_user_id} 在 {test_date} 的AC题目数量: {ac_count}")

