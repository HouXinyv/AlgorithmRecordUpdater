import json
import datetime

def load_users(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)["users"]

def get_yesterday():
    return datetime.date.today() - datetime.timedelta(days=1)

def col_idx_to_letter(idx):
    """将列索引(0为A)转为Excel列字母"""
    letters = ""
    while idx >= 0:
        letters = chr(idx % 26 + ord('A')) + letters
        idx = idx // 26 - 1
    return letters

def update_sheet(doc, leetcode, users, date):
    col_idx = date.day  # 1号->B(1), 2号->C(2), ...
    col_letter = col_idx_to_letter(col_idx)
    for user in users:
        row = user["row_number"]
        leetcode_id = user.get("leetcode")
        if leetcode_id:
            count = leetcode.get_ac_count(leetcode_id, date)
            cell = f"{col_letter}{row}"
            doc.set(cell, count)
    doc.save()

