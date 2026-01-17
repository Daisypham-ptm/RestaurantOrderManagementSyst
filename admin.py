import sqlite3

DB_PATH = "database/restaurant_menu.db"
def get_connection():
    return sqlite3.connect(DB_PATH)


def continue_or_back():
    while True:
        print("\n1. Continue")
        print("0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            return True
        elif choice == "0":
            return False
        else:
            print("Invalid choice")
def admin_menu():
    while True:
        print("\n===== ADMIN MENU =====")
        print("1. Manage Menu Items")
        print("2. Manage Categories")
        print("3. Manage Orders")
        print("4. Manage Users")
        print("5. View Reports")
        print("0. Exit")

        choice = input("Select option: ").strip()

        if choice == "1":
            manage_menu_items()
        elif choice == "2":
            manage_categories()
        elif choice == "3":
            manage_orders()
        elif choice == "4":
            manage_users()
        elif choice == "5":
            view_reports()
        elif choice == "0":
            print("Exit Admin Panel")
            break
        else:
            print("Invalid choice")
def manage_menu_items():
    while True:
        print("\n===== MANAGE MENU ITEMS =====")
        print("1. View Menu Items")
        print("2. Add Menu Item")
        print("3. Update Menu Item")
        print("4. Delete Menu Item")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            view_menu_items()
        elif choice == "2":
            add_menu_item()
        elif choice == "3":
            update_menu_item()
        elif choice == "4":
            delete_menu_item()
        elif choice == "0":
            break
        else:
            print("Invalid choice")
def view_menu_items():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT item_id, item_name, price, status
        FROM menu_items
    """)
    rows = cur.fetchall()
    conn.close()
    print("\n--- MENU ITEMS ---")
    for r in rows:
        print(f"ID:{r[0]} | Name:{r[1]} | Price:{r[2]} | Status:{r[3]}")
    input("\nPress Enter to go back...")
def add_menu_item():
    while True:
        try:
            category_id = int(input("Category ID: "))
            name = input("Item name: ").strip()
            desc = input("Description: ").strip()
            price = float(input("Price: "))
            status = input("Status (available/unavailable): ").strip()

            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO menu_items
                (category_id, item_name, description, price, status, avg_rating)
                VALUES (?, ?, ?, ?, ?, 0)
            """, (category_id, name, desc, price, status))
            conn.commit()
            conn.close()

            print("Menu item added successfully")
        except ValueError:
            print("Invalid input")

        if not continue_or_back():
            break
def update_menu_item():
    while True:
        view_menu_items()
        try:
            item_id = int(input("Item ID: "))
            name = input("New name: ").strip()
            desc = input("New description: ").strip()
            price = float(input("New price: "))
            status = input("New status: ").strip()

            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE menu_items
                SET item_name=?, description=?, price=?, status=?
                WHERE item_id=?
            """, (name, desc, price, status, item_id))
            conn.commit()
            conn.close()

            print("Menu item updated")
        except ValueError:
            print("Invalid input")

        if not continue_or_back():
            break
def delete_menu_item():
    while True:
        view_menu_items()
        try:
            item_id = int(input("Item ID to delete: "))
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM menu_items WHERE item_id=?", (item_id,))
            conn.commit()
            conn.close()
            print("Menu item deleted")
        except ValueError:
            print("Invalid ID")

        if not continue_or_back():
            break
def manage_categories():
    while True:
        print("\n===== MANAGE CATEGORIES =====")
        print("1. View Categories")
        print("2. Add Category")
        print("3. Update Category")
        print("4. Delete Category")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            view_categories()
        elif choice == "2":
            add_category()
        elif choice == "3":
            update_category()
        elif choice == "4":
            delete_category()
        elif choice == "0":
            break
        else:
            print("Invalid choice")
def view_categories():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT category_id, category_name, description FROM categories")
    rows = cur.fetchall()
    conn.close()

    print("\n--- CATEGORIES ---")
    for r in rows:
        print(f"ID:{r[0]} | Name:{r[1]} | Desc:{r[2]}")
    input("\nPress Enter to go back...")
def add_category():
    while True:
        name = input("Category name: ").strip()
        desc = input("Description: ").strip()

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO categories (category_name, description)
            VALUES (?, ?)
        """, (name, desc))
        conn.commit()
        conn.close()

        print("Category added")

        if not continue_or_back():
            break
def update_category():
    while True:
        view_categories()
        try:
            cid = int(input("Category ID: "))
            name = input("New name: ").strip()
            desc = input("New description: ").strip()

            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE categories
                SET category_name=?, description=?
                WHERE category_id=?
            """, (name, desc, cid))
            conn.commit()
            conn.close()

            print("Category updated")
        except ValueError:
            print("Invalid input")

        if not continue_or_back():
            break
def delete_category():
    while True:
        view_categories()
        try:
            cid = int(input("Category ID to delete: "))
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM categories WHERE category_id=?", (cid,))
            conn.commit()
            conn.close()
            print("Category deleted")
        except ValueError:
            print("Invalid ID")

        if not continue_or_back():
            break
def manage_orders():
    while True:
        print("\n===== MANAGE ORDERS =====")
        print("1. View Orders")
        print("2. Update Order Status")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            view_orders()
        elif choice == "2":
            update_order_status()
        elif choice == "0":
            break
        else:
            print("Invalid choice")
def view_orders():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT order_id, user_id, total_amount, status
        FROM orders
    """)
    rows = cur.fetchall()
    conn.close()

    print("\n--- ORDERS ---")
    for r in rows:
        print(f"ID:{r[0]} | User:{r[1]} | Total:{r[2]} | Status:{r[3]}")
    input("\nPress Enter to go back...")
def update_order_status():
    while True:
        view_orders()
        try:
            oid = int(input("Order ID: "))
            status = input("New status (Pending/Confirmed/Completed/Cancelled): ").strip()

            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE orders
                SET status=?
                WHERE order_id=?
            """, (status, oid))
            conn.commit()
            conn.close()

            print("Order status updated")
        except ValueError:
            print("Invalid input")

        if not continue_or_back():
            break
def manage_users():
    while True:
        print("\n===== MANAGE USERS =====")
        print("1. View Users")
        print("2. Update User")
        print("3. Delete User")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            view_users()
        elif choice == "2":
            update_user()
        elif choice == "3":
            delete_user()
        elif choice == "0":
            break
        else:
            print("Invalid choice")
def view_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, username, role FROM users")
    rows = cur.fetchall()
    conn.close()

    print("\n--- USERS ---")
    for r in rows:
        print(f"ID:{r[0]} | Username:{r[1]} | Role:{r[2]}")
    input("\nPress Enter to go back...")
def update_user():
    while True:
        view_users()
        try:
            uid = int(input("User ID: "))
            username = input("New username: ").strip()
            role = input("New role: ").strip()

            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE users
                SET username=?, role=?
                WHERE user_id=?
            """, (username, role, uid))
            conn.commit()
            conn.close()

            print("User updated")
        except ValueError:
            print("Invalid input")

        if not continue_or_back():
            break
def delete_user():
    while True:
        view_users()
        try:
            uid = int(input("User ID to delete: "))
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE user_id=?", (uid,))
            conn.commit()
            conn.close()
            print("User deleted")
        except ValueError:
            print("Invalid ID")

        if not continue_or_back():
            break
def view_reports():
    conn = get_connection()
    cur = conn.cursor()

    print("\n===== SYSTEM REPORT =====")
    cur.execute("SELECT COUNT(*) FROM orders")
    total_orders = cur.fetchone()[0]
    cur.execute("""
        SELECT SUM(total_amount)
        FROM orders
        WHERE status='Completed'
    """)
    revenue = cur.fetchone()[0] or 0
    cur.execute("""
        SELECT mi.item_name, SUM(oi.quantity) AS total_qty
        FROM order_items oi
        JOIN menu_items mi ON oi.item_id = mi.item_id
        GROUP BY mi.item_name
        ORDER BY total_qty DESC
        LIMIT 1
    """)
    best_seller = cur.fetchone()

    conn.close()

    print(f"Total Orders: {total_orders}")
    print(f"Total Revenue: {revenue}")
    if best_seller:
        print(f"Best Selling Item: {best_seller[0]} ({best_seller[1]} sold)")
    else:
        print("Best Selling Item: None")

    input("\nPress Enter to go back...")
if __name__ == "__main__":
    admin_menu()
