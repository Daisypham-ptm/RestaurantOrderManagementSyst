from datetime import datetime
from db import get_connection

def place_order(customer_id):
    """
    Places a new order for the given customer ID.
    USE CASE: place order
    """

    conn= get_connection()
    cur= conn.cursor()

    # Cart
    cur.execute("""
        SELECT c.item_id, c.quanity, m.price, m.item_name
        FROM cart_items c
        JOIN menu_items m ON c.item_id= m.item_id
        WHERE c.user_id= ?
    """, (customer_id,))
    cart_items= cur.fetchall()

    if not cart_items: 
        print(" Cart is empty")
        conn.close()
        return
    
    # reciver's  information
    print(f" ======== Receiver Information ========")
    receiver_name= input(" Receiver name: ")
    receiver_phone= input(" Receiver phone: ")
    receiver_address= input(" Receiver address: ")
    print(" ======================================")

    # payment method
    print(" Select payment method: ")
    print(" 1. Cash on delivery")
    print(" 2. Payment online")
    payment_choice= input("Choice (1/2): ")

    # total price calculation
    total_price= sum(item[2]* item[3] for item in cart_items)

    # create order 
    cur.execute("""
        INSERT INTO orders 
        (user_id, receiver_name, receiver_phone, receiver_address, payment_method, total_price, order_time, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
    """, (
        customer_id,
        receiver_name,
        receiver_phone,
        receiver_address,
        total_price,
        payment_choice,
        "new",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    order_id= cur.lastrowid

    # insert order into table 
    for item in cart_items:
        cur.execute("""
            INSERT INTO order_items (order_id, item_id, quantity, price)
            VALUES (?, ?, ?, ?)
    """, (
            order_id,
            item[0],
            item[1],
            item[2],
            item[3]
    ))
        # Update stock in menu_items table
        cur.execute("""
            UPDATE menu_items
            SET order_count= order_count+ ?
            WHERE item_id= ?
    """, (item[3], item[0]))
        
    # clear cart
    cur.execute("""
        DELETE FROM cart_items
        WHERE user_id= ?
    """, (customer_id,)
    )

    conn.commit()
    conn.close()

    print(" Order successfully")
    print(f" Order ID: {order_id}")
    print( f" Total Price: ${total_price:.2f}")
     


def view_orders(customer_id):
    conn= get_connection()
    cur= conn.cursor()

    cur.exxecute("""
        SELECT order_id, status, total_price, order_time
        FROM orders 
        WHERE user_id= ?
        ORDER BY order_time DESC
    """,(customer_id))

    orders= cur.fetchall()
    conn.close()

    if not orders:
        print(" No orders found.")
        return
    
    print(" ======== Your Orders ========")
    for order in orders:
        print(
              f"Order ID: {order[0]} |"
              f"Status: {order[1]} |"
              f"Total Price: {order[2]:.2f} |"
              f"Order Time: {order[3]}"
              )
        
    
def cancel_order(customer_id):
    conn= get_connection()
    cur= conn.cursor()

    order_id= input(" Enter Order ID to cancel: ")

    cur.execute("""
        SELECT status
        FROM orders
        WHERE order_id= ? AND user_id= ?
    """, (order_id, customer_id))

    result= cur.fetchone()

    if not result:
        print("Order not found.")
        conn.close()
        return
    
    if result[0] != "new":
        print(" Only new orders can be canceled.")
        conn.close()
        return
    
    cur.execute("""
        UPDATE orders
        SET status= "canceled"
        WHERE order_id= ? AND user_id= ?
        """, (order_id))
    
    conn.commit()
    conn.close()
    print(" Order canceled successfully.")


def view_order_history(customer_id):
    conn= get_connection()
    cur= conn.cursor()

    cur.execute("""
        SRLECT order_id, status, total_price, order_time
        FROM orders
        WHERE user_id=?
        ORDER BY order_time DESC
        """, (customer_id,))
    
    orders= cur.fetchall()
    conn.close()

    if not orders:
        print(" No order history found.")
        return
    
    print(" ======== Order History ========")
    for order in orders:
        print(
            f"Order ID: {order[0]} |"
            f"Status: {order[1]} |"
            f"Total Price: {order[2]:.2f} |"
            f"Order Time: {order[3]}"
        )

    cur.execute("""
        SELECT item_name, unit_price, quantity
        FROM order_items
        WHERE order_id= ?
    """, (order[0],))

    items= cur.fetchall()
    for item in items:
        print(
            f"  Item: {item[0]} |"
            f"Unit Price: {item[1]:.2f} |"
            f"Quantity: {item[2]}"
        )

    conn.close()