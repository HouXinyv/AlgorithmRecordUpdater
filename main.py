import time
import datetime
import schedule
import logging
import os
from platforms.leetcode import LeetCodePlatform
from platforms.codeforces import CodeforcesPlatform
from platforms.vjudge import VJudgePlatform
from platforms.luogu import LuoguPlatform
from platforms.nowcoder import NowCoderPlatform
from doc_updater.tencent_doc import TencentDocUpdater
from util.util_fun import load_users, col_idx_to_letter, load_config

# 创建logs目录（如果不存在）
os.makedirs('logs', exist_ok=True)

# 配置日志同时输出到控制台和文件
log_file = f'logs/record_updater_{datetime.datetime.now().strftime("%Y-%m-%d")}.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main(debug=False):
    data = load_users()  # data 中包含 "users" 和 "user_order"
    user_order = data.get("user_order", list(data["users"].keys()))
    config = load_config()
    doc = TencentDocUpdater(
        config["doc"]["tencentdoc"]["url"],
        cookies=config["doc"]["tencentdoc"]["cookie"]
    )

    # 创建各平台实例，不再需要传递 cookies
    leetcode = LeetCodePlatform()
    codeforces = CodeforcesPlatform()
    vjudge = VJudgePlatform()
    luogu = LuoguPlatform()
    nowcoder = NowCoderPlatform()

    platforms = {
        "leetcode": leetcode,
        "vjudge": vjudge,
        "codeforces": codeforces,
        "luogu": luogu,
        "nowcoder": nowcoder
    }

    def job():
        # 获取昨天的数据
        date = datetime.date.today()   - datetime.timedelta(days=1)
        col_idx = date.day + 2  # 列号从3开始
        col_letter = col_idx_to_letter(col_idx)

        logger.info(f"开始更新 {date} 的数据...")

        for idx, nickname in enumerate(user_order):
            user = data["users"][nickname]
            row = idx + 2  # 行号从2开始
            total = 0
            platform_counts = []

            for pf_name, pf in platforms.items():
                pf_id = user.get(pf_name)
                if pf_id:
                    count = pf.get_ac_count(pf_id, date)
                    if count > 0:
                        platform_counts.append(f"{pf_name}: {count}")
                    total += count

            # 三题哥的打死也不说id ......
            if nickname == "三题哥":
                total = 3
                platform_counts.append(f"leetcode: 3")

            platform_str = "\t".join(platform_counts) if platform_counts else "未做题"
            logger.info(f"{date}\t{nickname:<18}\t做题数\t{total:<3}\t({platform_str})")

            cell = f"{col_letter}{row}"
            doc.set(cell, total)

        doc.save()
        logger.info(f"已更新 {date} 的数据到腾讯文档。")

    if debug:
        logger.info("以调试模式运行...")
        job()
    else:
        logger.info("腾讯文档已打开，等待定时任务...")
        schedule.every().day.at("03:00").do(job)

        while True:
            schedule.run_pending()
            time.sleep(max(60, schedule.idle_seconds()))


if __name__ == "__main__":
    main(debug=True)
