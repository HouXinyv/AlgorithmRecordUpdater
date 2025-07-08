import requests
import datetime
import time
from bs4 import BeautifulSoup

from platforms.base import BasePlatform


class NowCoderPlatform(BasePlatform):
    def __init__(self):
        """
        NowCoder平台初始化
        """
        super().__init__("NowCoder")

    def get_ac_count(self, user_id: str, date: datetime.date) -> int:
        """
        获取指定用户在指定日期的AC题目数量
        :param user_id: NowCoder用户ID
        :param date: 日期对象
        :return: 通过的题目数量
        """
        url = self.url.format(user_id)
        try:
            resp = requests.get(url, headers=self.headers)
            resp.raise_for_status()  # 对于错误状态码抛出异常
            soup = BeautifulSoup(resp.text, 'html.parser')

            # 找到表格的tbody，包含提交记录
            tbody = soup.find('tbody')
            if not tbody:
                return 0

            # 使用基类方法获取时间戳
            start_ts = self.get_start_timestamp(date)
            end_ts = self.get_end_timestamp(date)

            # 统计唯一通过的题目
            problem_ids = set()
            for row in tbody.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) < 9:
                    continue

                # 检查提交状态是否为“答案正确”
                status = cols[2].text.strip()
                if status != "答案正确":
                    continue

                # 获取题目ID（从题目链接中提取）
                problem_link = cols[1].find('a')['href']
                problem_id = problem_link.split('/')[-1]

                # 获取提交时间并转换为时间戳
                submit_time_str = cols[8].text.strip()
                submit_time = datetime.datetime.strptime(submit_time_str, '%Y-%m-%d %H:%M:%S')
                submit_ts = int(time.mktime(submit_time.timetuple()))

                # 检查提交时间是否在指定日期范围内
                if start_ts <= submit_ts < end_ts:
                    problem_ids.add(problem_id)

            return len(problem_ids)
        except (requests.RequestException, ValueError, AttributeError):
            return 0  # 网络、解析或时间格式错误时返回0


if __name__ == "__main__":
    """
    测试NowCoderPlatform的get_ac_count方法
    """
    platform = NowCoderPlatform()
    test_user_id = "9776352"  # 示例用户ID
    test_date = datetime.date(2024, 8, 30)  # 示例日期
    ac_count = platform.get_ac_count(test_user_id, test_date)
    print(f"用户 {test_user_id} 在 {test_date} 的AC题目数量: {ac_count}")

