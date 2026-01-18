from order import place_order, view_orders, cancel_order, view_order_history

# dùng user_id tồn tại trong DB
user_id = 2

print("=== TEST place_order ===")
place_order(user_id)

print("\n=== TEST view_orders ===")
view_orders(user_id)

print("\n=== TEST view_order_history ===")
view_order_history(user_id)

print("\n=== TEST cancel_order ===")
cancel_order(user_id)