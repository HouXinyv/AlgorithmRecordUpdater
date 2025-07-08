import datetime
from abc import ABC
from util.util_fun import load_config


class BasePlatform(ABC):
    def __init__(self, name: str):
        """
        平台基类，所有平台实现需继承此类
        """
        self.name = name.lower()
        self.config = load_config()
        self.headers = self.build_headers()
        self.url = self.config['platforms'][self.name]['url']

    def build_headers(self):
        """构建请求头"""
        # 合并通用headers和平台特定headers
        headers = self.config['common_header'].copy()
        platform_headers = self.config['platforms'][self.name].get('header', {})
        headers.update(platform_headers)

        # 如果有cookies，添加到headers中
        cookies = self.config['platforms'][self.name].get('cookie', {})
        if cookies:
            headers['Cookie'] = '; '.join(f"{k}={v}" for k, v in cookies.items())

        return headers

    @staticmethod
    def get_ac_count(self, user_id: str, date: datetime.date) -> int:
        """
        获取指定用户在指定日期的AC题目数量
        :param self:
        :param user_id: 用户在平台的唯一标识
        :param date: 日期对象
        :return: 通过题目数量
        """

    def get_start_timestamp(self, date: datetime.date) -> int:
        """
        获取指定日期的起始时间戳（加3小时，单位：秒）
        :param date: 日期对象
        :return: 起始时间戳（秒）
        """
        dt = datetime.datetime.combine(date, datetime.time.min) + datetime.timedelta(hours=3)
        return int(dt.timestamp())

    def get_end_timestamp(self, date: datetime.date) -> int:
        """
        获取指定日期的结束时间戳（加3小时，单位：秒）
        :param date: 日期对象
        :return: 结束时间戳（秒）
        """
        dt = datetime.datetime.combine(date + datetime.timedelta(days=1), datetime.time.min) + datetime.timedelta(
            hours=3)
        return int(dt.timestamp())

    def get_pf_name(self) -> str:
        """
        获取平台名称
        :return: 平台名称
        """
        return self.name
