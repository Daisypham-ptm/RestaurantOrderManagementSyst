import sqlite3
from typing import List, Optional, Dict

# MODEL
class MenuItem:
    """MenuItem Model"""
    def __init__(
        self,
        item_id: int,
        category_id: int,
        item_name: str,
        description: str,
        price: float,
        status: str,
        order_count: int = 0,
        avg_rating: float = 0.0
    ):
        self.item_id = item_id
        self.category_id = category_id
        self.item_name = item_name
        self.description = description
        self.price = price
        self.status = status
        self.order_count = order_count
        self.avg_rating = avg_rating

    def __str__(self):
        return f"{self.item_name} - {self.price:,.0f} VND"
# BUSINESS LOGIC

class MenuManager:
    """Menu Management Class"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        except sqlite3.Error as err:
            print(f"Database connection error: {err}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()

    def view_menu(self, category_id: Optional[int] = None) -> List[MenuItem]:
        """View menu items"""
        try:
            query = """
                SELECT m.*
                FROM menu_items m
                JOIN categories c ON m.category_id = c.category_id
                WHERE m.status = 'available'
            """
            params = []

            if category_id is not None:
                query += " AND m.category_id = ?"
                params.append(category_id)

            query += " ORDER BY m.item_name ASC"

            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()

            menu_items = []
            for row in rows:
                menu_items.append(
                    MenuItem(
                        item_id=row["item_id"],
                        category_id=row["category_id"],
                        item_name=row["item_name"],
                        description=row["description"],
                        price=row["price"],
                        status=row["status"],
                        order_count=0,
                        avg_rating=0.0 
                    )
                )

            return menu_items

        except sqlite3.Error as err:
            print(f"Database error: {err}")
            return []

    def search_menu(self, keyword: str) -> List[MenuItem]:
        """Search menu items"""
        try:
            query = """
                SELECT m.*
                FROM menu_items m
                JOIN categories c ON m.category_id = c.category_id
                WHERE m.status = 'available'
                AND (
                    m.item_name LIKE ?
                    OR m.description LIKE ?
                )
                ORDER BY m.item_name ASC
            """

            pattern = f"%{keyword}%"
            self.cursor.execute(query, (pattern, pattern))
            rows = self.cursor.fetchall()

            menu_items = []
            for row in rows:
                menu_items.append(
                    MenuItem(
                        item_id=row["item_id"],
                        category_id=row["category_id"],
                        item_name=row["item_name"],
                        description=row["description"],
                        price=row["price"],
                        status=row["status"],
                        order_count=0,
                        avg_rating=0.0
                    )
                )

            return menu_items

        except sqlite3.Error as err:
            print(f"Database error: {err}")
            return []

    

    def view_food_detail(self, item_id: int) -> Optional[Dict]:
        """View food detail"""
        try:
            query = """
                SELECT m.*, c.category_name
                FROM menu_items m
                JOIN categories c ON m.category_id = c.category_id
                WHERE m.item_id = ?
            """
            self.cursor.execute(query, (item_id,))
            row = self.cursor.fetchone()

            if not row:
                return None

            return {
                "item_id": row["item_id"],
                "item_name": row["item_name"],
                "category_name": row["category_name"],
                "description": row["description"],
                "price": row["price"],
                "status": row["status"]
            }

        except sqlite3.Error as err:
            print(f"Database error: {err}")
            return None

    

    def get_categories(self) -> List[Dict]:
        """Get all categories"""
        try:
            query = "SELECT * FROM categories ORDER BY display_order ASC"
            self.cursor.execute(query)
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as err:
            print(f"Database error: {err}")
            return []



# UI DISPLAY FUNCTIONS


def display_view_menu(items: List[MenuItem]):
    print("\n" + "=" * 70)
    print("VIEW MENU".center(70))
    print("=" * 70)

    if not items:
        print("No food items found.")
        print("=" * 70)
        return

    print(f"{'Food ID':<10} {'Name':<30} {'Price':<15} {'Status':<12}")
    print("-" * 70)

    for item in items:
        print(
            f"{item.item_id:<10} "
            f"{item.item_name:<30} "
            f"{item.price:>12,.0f} VND "
            f"{item.status:<12}"
        )

    print("=" * 70)


def display_search_menu(keyword: str, items: List[MenuItem]):
    print(f"\nSearch keyword: {keyword}")

    if not items:
        print("No matching items found.")
        return

    print(f"\nResults found: {len(items)} item(s)")
    print(f"{'Food ID':<10} {'Name':<30} {'Price':<15} {'Status':<12}")
    print("-" * 70)

    for item in items:
        print(
            f"{item.item_id:<10} "
            f"{item.item_name:<30} "
            f"{item.price:>12,.0f} VND "
            f"{item.status:<12}"
        )


def display_food_detail(detail: Optional[Dict]):
    if not detail:
        print("\nFood item not found!")
        return

    print("\n" + "=" * 70)
    print("FOOD DETAIL".center(70))
    print("=" * 70)

    print(f"Name:        {detail['item_name']}")
    print(f"Category:    {detail['category_name']}")
    print(f"Price:       {detail['price']:,.0f} VND")
    print(f"Description: {detail['description']}")
    print(f"Status:      {detail['status']}")

    print("=" * 70)


