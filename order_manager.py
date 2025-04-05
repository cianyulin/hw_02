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

def add_order(orders: list) -> str:
    """add_order(orders: list) -> str：新增訂單至列表，若訂單編號重複則返回錯誤訊息"""
    order_id = input("請輸入訂單編號：").strip().upper()
    if any(order["order_id"] == order_id for order in orders):
        return f"=> 錯誤：訂單編號 {order_id} 已存在！"

    customer = input("請輸入顧客姓名：").strip()
    items = []

    while True:
        name = input("請輸入訂單項目名稱（輸入空白結束）：").strip()
        if not name:
            break
        try:
            price = int(input("請輸入價格："))
            if price < 0:
                print("=> 錯誤：價格不能為負數，請重新輸入")
                continue
        except ValueError:
            print("=> 錯誤：價格或數量必須為整數，請重新輸入")
            continue

        try:
            quantity = int(input("請輸入數量："))
            if quantity <= 0:
                print("=> 錯誤：數量必須為正整數，請重新輸入")
                continue
        except ValueError:
            print("=> 錯誤：價格或數量必須為整數，請重新輸入")
            continue

        items.append({"name": name, "price": price, "quantity": quantity})

    if not items:
        return "=> 至少需要一個訂單項目"

    orders.append({
        "order_id": order_id,
        "customer": customer,
        "items": items
    })

    return f"=> 訂單 {order_id} 已新增！"

"""測試新增訂單的功能"""
def main():
    orders = load_data(INPUT_FILE)
    result = add_order(orders)
    print(result)
    if "已新增" in result:
        save_orders(INPUT_FILE, orders)

if __name__ == "__main__":
    main()