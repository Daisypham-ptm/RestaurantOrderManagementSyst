import sqlite3

DB_PATH = "database/restaurant_menu.db"


# ================== CART ITEM CLASS ==================
class CartItem:
    def __init__(self, food_id, food_name, price, quantity):
        self.food_id = food_id
        self.food_name = food_name
        self.price = price
        self.quantity = quantity
        self.total = price * quantity


# ================== CART CLASS ==================
class Cart:
    def __init__(self, user_id):
        self.user_id = user_id

    def connect_db(self):
        return sqlite3.connect(DB_PATH)

    # ---------- ADD TO CART ----------
    def add_to_cart(self, food_id, quantity):
        conn = self.connect_db()
        cur = conn.cursor()

        # Check food exists
        cur.execute("""
            SELECT item_name, price
            FROM menu_items
            WHERE item_id = ? AND status = 'available'
        """, (food_id,))
        food = cur.fetchone()

        if not food:
            print("Food not found or unavailable.")
            conn.close()
            return

        food_name, price = food
        subtotal = price * quantity

        # Check if item already in cart
        cur.execute("""
            SELECT cart_item_id, quantity
            FROM cart_items
            WHERE user_id = ? AND item_id = ?
        """, (self.user_id, food_id))

        existing = cur.fetchone()

        if existing:
            cart_item_id, old_qty = existing
            new_qty = old_qty + quantity
            new_subtotal = new_qty * price

            cur.execute("""
                UPDATE cart_items
                SET quantity = ?, subtotal = ?
                WHERE cart_item_id = ?
            """, (new_qty, new_subtotal, cart_item_id))
        else:
            cur.execute("""
                INSERT INTO cart_items (user_id, item_id, quantity, subtotal)
                VALUES (?, ?, ?, ?)
            """, (self.user_id, food_id, quantity, subtotal))

        conn.commit()
        conn.close()
        print("Added to cart successfully.")

    # ---------- UPDATE CART ----------
    def update_cart(self, food_id, new_quantity):
        conn = self.connect_db()
        cur = conn.cursor()

        if new_quantity <= 0:
            print("Quantity must be greater than 0.")
            conn.close()
            return

        cur.execute("""
            SELECT price
            FROM menu_items
            WHERE item_id = ?
        """, (food_id,))
        price_data = cur.fetchone()

        if not price_data:
            print("Food not found.")
            conn.close()
            return

        price = price_data[0]
        new_subtotal = price * new_quantity

        cur.execute("""
            UPDATE cart_items
            SET quantity = ?, subtotal = ?
            WHERE user_id = ? AND item_id = ?
        """, (new_quantity, new_subtotal, self.user_id, food_id))

        conn.commit()
        conn.close()
        print("Cart updated successfully.")

    # ---------- REMOVE FROM CART ----------
    def remove_from_cart(self, food_id):
        conn = self.connect_db()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM cart_items
            WHERE user_id = ? AND item_id = ?
        """, (self.user_id, food_id))

        conn.commit()
        conn.close()
        print("Item removed from cart.")

    # ---------- VIEW CART ----------
    def view_cart(self):
        conn = self.connect_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT m.item_id, m.item_name, m.price, c.quantity, c.subtotal
            FROM cart_items c
            JOIN menu_items m ON c.item_id = m.item_id
            WHERE c.user_id = ?
        """, (self.user_id,))

        items = cur.fetchall()

        if not items:
            print("Your cart is empty.")
            conn.close()
            return

        print("\n===== YOUR CART =====")
        print("{:<8} {:<20} {:<10} {:<10} {:<10}".format(
            "ID", "Food Name", "Price", "Qty", "Total"
        ))

        for item in items:
            print("{:<8} {:<20} {:<10} {:<10} {:<10}".format(*item))

        print("-----------------------------")
        print("Total Amount:", self.calculate_total())
        conn.close()

    # ---------- CALCULATE TOTAL ----------
    def calculate_total(self):
        conn = self.connect_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT SUM(subtotal)
            FROM cart_items
            WHERE user_id = ?
        """, (self.user_id,))

        total = cur.fetchone()[0]
        conn.close()

        return total if total else 0
