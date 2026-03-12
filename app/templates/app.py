from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = "shopwave-secret-2024"

PRODUCTS = [
    {"id": 1, "name": "Wireless Headphones", "price": 79.99,  "emoji": "🎧", "category": "Electronics"},
    {"id": 2, "name": "Running Shoes",        "price": 59.99,  "emoji": "👟", "category": "Footwear"},
    {"id": 3, "name": "Leather Backpack",     "price": 89.99,  "emoji": "🎒", "category": "Bags"},
    {"id": 4, "name": "Smart Watch",          "price": 199.99, "emoji": "⌚", "category": "Electronics"},
    {"id": 5, "name": "Coffee Maker",         "price": 49.99,  "emoji": "☕", "category": "Kitchen"},
    {"id": 6, "name": "Yoga Mat",             "price": 24.99,  "emoji": "🧘", "category": "Sports"},
]


@app.route("/")
def index():
    cart   = session.get("cart", {})
    total  = sum(v for v in cart.values())
    return render_template("index.html", products=PRODUCTS, cart_count=total)


@app.route("/cart")
def cart():
    cart  = session.get("cart", {})
    items = []
    total = 0
    for pid, qty in cart.items():
        p = next((x for x in PRODUCTS if x["id"] == int(pid)), None)
        if p:
            subtotal = p["price"] * qty
            total   += subtotal
            items.append({**p, "qty": qty, "subtotal": round(subtotal, 2)})
    cart_count = sum(cart.values())
    return render_template("cart.html", items=items, total=round(total, 2), cart_count=cart_count)


@app.route("/add/<int:pid>")
def add(pid):
    cart      = session.get("cart", {})
    cart[str(pid)] = cart.get(str(pid), 0) + 1
    session["cart"] = cart
    return redirect(url_for("index"))


@app.route("/remove/<int:pid>")
def remove(pid):
    cart = session.get("cart", {})
    cart.pop(str(pid), None)
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)