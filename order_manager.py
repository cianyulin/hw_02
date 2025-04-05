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

def save_orders(filename: str, orders: list) -> None:
    """save_orders(filename: str, orders: list) -> None：將訂單列表存入 JSON 檔案"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=4, ensure_ascii=False)

def calculate_order_total(order: dict) -> int:
    """calculate_order_total(order: dict) -> int：計算單筆訂單的總金額"""
    return sum(item["price"] * item["quantity"] for item in order["items"])

orders = load_data("orders.json")
"""印出總金額看看"""
for order in orders:
    total = calculate_order_total(order)
    print(f"顧客：{order['customer']}，總金額：{total}")
