from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd, os, urllib.parse
from markupsafe import Markup


APP_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(APP_DIR, "..", "products.csv") if not os.path.exists(os.path.join(APP_DIR, "products.csv")) else os.path.join(APP_DIR, "products.csv")

# If you want to keep product CSV with the app, copy /mnt/data/products.csv into the project folder.
if not os.path.exists(CSV_PATH):
    # fallback to absolute path where the user placed the file by default
    CSV_PATH = "/mnt/data/products.csv"

df = pd.read_csv(CSV_PATH).fillna('')
df['product_id'] = df['product_id'].astype(str)

def placeholder_image_url(name, size='300'):
    # use a simple placeholder service; spaces -> + for nicer labels
    label = urllib.parse.quote_plus(name)
    return f"https://via.placeholder.com/{size}.png?text={label}"

def product_dict(row):
    return {
        'product_id': str(row['product_id']),
        'product_name': row['product_name'],
        'category': row.get('category', ''),
        'related_products': [p.strip() for p in str(row.get('related_products', '')).split(',') if p.strip()],
        'image': f"/static/images/{row.get('image_file')}" 
                 if row.get('image_file') else placeholder_image_url(row['product_name'], size='300')
    }


PRODUCTS = {str(r['product_id']): product_dict(r) for r in df.to_dict(orient='records')}

app = Flask(__name__)
app.secret_key = 'change-me-to-a-secret-key'


def get_cart():
    return session.get('cart', [])

def save_cart(cart):
    session['cart'] = cart

def recommend_from_cart(cart):
    # gather related product ids from related_products, and fill with same-category products not in cart
    recs = []
    seen = set(cart)
    for pid in cart:
        p = PRODUCTS.get(pid)
        if not p: continue
        for r in p['related_products']:
            if r not in seen and r in PRODUCTS:
                recs.append(r)
                seen.add(r)
    # fill with category-based popular choices
    if len(recs) < 6:
        # pick products from same categories as items in cart
        cats = {PRODUCTS[p]['category'] for p in cart if p in PRODUCTS}
        for pid, p in PRODUCTS.items():
            if pid in seen: continue
            if p['category'] in cats:
                recs.append(pid)
                seen.add(pid)
            if len(recs) >= 6:
                break
    # final fallback: top items
    if len(recs) < 6:
        for pid in PRODUCTS:
            if pid in seen: continue
            recs.append(pid)
            seen.add(pid)
            if len(recs) >= 6: break
    return [PRODUCTS[r] for r in recs[:6]]


@app.route('/')
def home():
    q = request.args.get('q', '').strip().lower()
    cart = get_cart()
    items = list(PRODUCTS.values())
    if q:
        items = [p for p in items if q in p['product_name'].lower() or q in p['category'].lower()]
    recommendations = recommend_from_cart(cart) if cart else items[:6]
    return render_template('home.html', products=items, cart=cart, recommendations=recommendations, query=q)


@app.route('/add_to_cart/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    cart = get_cart()
    if product_id not in cart and product_id in PRODUCTS:
        cart.append(product_id)
        save_cart(cart)
    return redirect(url_for('home'))

@app.route('/remove_from_cart/<product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = get_cart()
    if product_id in cart:
        cart.remove(product_id)
        save_cart(cart)
    return redirect(url_for('home'))

@app.route('/cart')
def view_cart():
    cart = get_cart()
    items = [PRODUCTS[p] for p in cart if p in PRODUCTS]
    recommendations = recommend_from_cart(cart) if cart else []
    return render_template('cart.html', items=items, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
