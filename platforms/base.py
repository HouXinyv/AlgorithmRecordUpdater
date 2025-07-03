import datetime

class PlatformAdapterBase:
    def get_ac_count(self, user_id: str, date: datetime.date) -> int:
        """
        获取指定用户在指定日期的AC题目数量
        :param user_id: 用户在平台的唯一标识
        :param date: 日期对象
        :return: 通过题目数量
        """
        raise NotImplementedError("子类需实现该方法")

