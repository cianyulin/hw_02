import json
"""只有 import JSON 模組：使用到 json.load() 和 json.dump() 函數。"""

"""在程式開頭定義"""
INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"

def load_data(filename: str) -> list:
    """load_data(filename: str) -> list：從 JSON 檔案載入資料，若檔案不存在則返回空列表"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

orders = load_data(INPUT_FILE)
print(orders)