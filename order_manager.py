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

#orders = load_data(INPUT_FILE)
#print(orders)

def save_orders(filename: str, orders: list) -> None:
    """save_orders(filename: str, orders: list) -> None：將訂單列表存入 JSON 檔案"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=4, ensure_ascii=False)

def calculate_order_total(order: dict) -> int:
    """calculate_order_total(order: dict) -> int：計算單筆訂單的總金額"""
    return sum(item["price"] * item["quantity"] for item in order["items"])

#orders = load_data("orders.json")
#"""印出總金額看看"""
#for order in orders:
#    total = calculate_order_total(order)
#    print(f"顧客：{order['customer']}，總金額：{total}")

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
def count_chinese_chars(text):
    """計算中文字數（不含英數字）"""
    return sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
def print_order_report(data: list, title="訂單報表", single=False):
    """print_order_report(data, title="訂單報表", single=False)：
    顯示訂單報表，可顯示單筆訂單或多筆訂單。
    參數 single 指定是否為單筆訂單。"""
    if single:
        print(f"\n==================== 出餐訂單 ====================")
    else:
        print(f"\n==================== {title} ====================")

    for idx, order in enumerate(data, 1):
        if not single:
            print(f"訂單 #{idx}")
        print(f"訂單編號: {order['order_id']}")
        print(f"客戶姓名: {order['customer']}")
        print("--------------------------------------------------")
        # 使用F字串來對齊
        print(f"{'商品名稱'}\t{'單價'}\t{'數量'}\t{'小計'}")
        print("--------------------------------------------------")
        total = 0
        #一直對齊不了有夠生氣，發現是因為品名少於四個字就會造成排版錯誤
        #所以把不到四個字的加空格加到四個
        for item in order["items"]:
            name = item["name"]
            name_display = name  # 不要直接改 item['name']，用一個新變數

            chinese_len = count_chinese_chars(name)
            if chinese_len == 1:
                name_display += ' ' * 6
            elif chinese_len == 2:
                name_display += ' ' * 4
            elif chinese_len == 3:
                name_display += ' ' * 2
            # 四個以上就不加空格

            subtotal = item["price"] * item["quantity"]
            print(f"{name_display}\t{item['price']}\t{item['quantity']}\t{subtotal}")
            total += subtotal
        print("--------------------------------------------------")
        print(f"訂單總額: {total:,}")
        print("--------------------------------------------------")

def process_order(orders: list) -> tuple:
    """處理訂單並轉移至已出餐列表"""
    if not orders:
        return "=> 無待處理訂單", None

    print("\n======== 待處理訂單列表 ========")
    for i, order in enumerate(orders, start=1):
        print(f"{i}. 訂單編號: {order['order_id']} - 客戶: {order['customer']}")
    print("================================")

    while True:
        sel = input("請選擇要出餐的訂單編號 (輸入數字或按 Enter 取消): ").strip()

        if sel == "":
            return "=> 取消出餐處理", None

        try:
            index = int(sel) - 1  # 使用者輸入的是從 1 開始，所以要 -1
            if 0 <= index < len(orders):
                # 取出並移除該筆訂單
                order = orders.pop(index)

                # 讀取已完成的訂單
                done_orders = load_data(OUTPUT_FILE)
                # 超崩潰的一直卡在這邊，結果是output那個JSON檔不能完全是空的，要至少加入[]
                done_orders.append(order)

                # 儲存回檔案
                save_orders(OUTPUT_FILE, done_orders)

                return f"=> 訂單 {order['order_id']} 已出餐完成", order
            else:
                print(f"=> 錯誤：請輸入 1 ~ {len(orders)} 之間的數字")
        except ValueError:
            print(f"=> 錯誤：無法將輸入的內容轉換為數字（你輸入的是:「{sel}」）")


def main():
    """主程式流程"""
    while True:
        print("***************選單***************")
        print("1. 新增訂單")
        print("2. 顯示訂單報表")
        print("3. 出餐處理")
        print("4. 離開")
        print("**********************************")
        choice = input("請選擇操作項目(Enter 離開)：")

        if choice == "":
            break
        elif choice == "1":
            orders = load_data(INPUT_FILE)
            result = add_order(orders)
            print(result)
            if result.startswith("=> 訂單"):
                save_orders(INPUT_FILE, orders)
        elif choice == "2":
            orders = load_data(INPUT_FILE)
            print_order_report(orders)
        elif choice == "3":
            orders = load_data(INPUT_FILE)
            result, order = process_order(orders)
            print(result)
            if order:
                print_order_report([order], title="出餐訂單", single=True)
                save_orders(INPUT_FILE, orders)
        elif choice == "4":
            break
        else:
            print("=> 請輸入有效的選項（1-4）")

if __name__ == "__main__":
    main()