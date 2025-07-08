import json
import datetime

def load_users():
    with open('config/users.json', "r", encoding="utf-8") as f:
        return json.load(f)

def load_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)

def col_idx_to_letter(idx):
    """将列索引(1为A)转为Excel列字母"""
    letters = ""
    while idx > 0:
        letters = chr(idx % 26 -1 + ord('A')) + letters
        idx = idx // 26
    return letters

if __name__ == "__main__":
    print(col_idx_to_letter(1))
    print(col_idx_to_letter(27))
