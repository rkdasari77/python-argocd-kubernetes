from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = "ecommerce-secret-key-2024"

PRODUCTS = [
    {"id": 1, "name": "Wireless Headphones", "price": 79.99, "category": "Electronics", "image": "🎧", "rating": 4.5, "reviews": 128},
    {"id": 2, "name": "Running Shoes", "price": 59.99, "category": "Footwear", "image": "👟", "rating": 4.7, "reviews": 94},
    {"id": 3, "name": "Leather Backpack", "price": 89.99, "category": "Bags", "image": "🎒", "rating": 4.3, "reviews": 67},
    {"id": 4, "name": "Smart Watch", "price": 199.99, "category": "Electronics", "image": "⌚", "rating": 4.6, "reviews": 213},
    {"id": 5, "name": "Sunglasses", "price": 34.99, "category": "Accessories", "image": "🕶️", "rating": 4.2, "reviews": 45},
    {"id": 6, "name": "Coffee Maker", "price": 49.99, "category": "Kitchen", "image": "☕", "rating": 4.8, "reviews": 301},
    {"id": 7, "name": "Yoga Mat", "price": 24.99, "category": "Sports", "image": "🧘", "rating": 4.4, "reviews": 88},
    {"id": 8, "name": "Mechanical Keyboard", "price": 119.99, "category": "Electronics", "image": "⌨️", "rating": 4.7, "reviews": 156},
]

@app.route("/")
def index():
    category = request.args.get("category", "All")
    search = request.args.get("search", "")
    cart = session.get("cart", {})
    cart_count = sum(cart.values())

    filtered = PRODUCTS
    if category != "All":
        filtered = [p for p in PRODUCTS if p["category"] == category]
    if search:
        filtered = [p for p in filtered if search.lower() in p["name"].lower()]

    categories = ["All"] + sorted(set(p["category"] for p in PRODUCTS))
    return render_template("index.html", products=filtered, categories=categories,
                           selected=category, search=search, cart_count=cart_count)

@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    cart_items = []
    total = 0
    for pid, qty in cart.items():
        product = next((p for p in PRODUCTS if p["id"] == int(pid)), None)
        if product:
            subtotal = product["price"] * qty
            total += subtotal
            cart_items.append({**product, "qty": qty, "subtotal": subtotal})
    return render_template("cart.html", cart_items=cart_items, total=total, cart_count=len(cart))

@app.route("/add/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart
    return redirect(url_for("index"))

@app.route("/remove/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    key = str(product_id)
    if key in cart:
        del cart[key]
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/health")
def health():
    return {"status": "healthy", "service": "ecommerce-app"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
