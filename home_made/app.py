from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure random key

# Helper functions for user storage in JSON
USERS_FILE = os.path.join(os.path.dirname(__file__), 'data', 'users.json')
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r') as f:
        try:
            return json.load(f)
        except Exception:
            return []
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)


# ---------- ROUTES ----------

@app.route('/')
def home():
    if not session.get('user'):
        return redirect(url_for('signup'))
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/snacks')
def snacks():
    snacks_products = []
    for p in products_fallback['snacks']:
        if '500' in p['weights']:
            price = p['weights']['500']
            w = '500'
            snacks_products.append({
                'id': int(f"{p['id']}{w}"),
                'base_id': p['id'],
                'name': f"{p['name']} {w}g",
                'price': price,
                'desc': 'Crispy, crunchy, and delicious snacks for every occasion.',
                'type': 'Snacks',
                'veg': True,
                'stock': 20,
                'category': 'snacks',
                'weight': w
            })
    return render_template('snacks.html', products=snacks_products, category='snacks')

@app.route('/veg-pickles')
def veg_pickles():
    veg_products = []
    for p in products_fallback['veg_pickles']:
        if '500' in p['weights']:
            price = p['weights']['500']
            w = '500'
            veg_products.append({
                'id': int(f"{p['id']}{w}"),
                'base_id': p['id'],
                'name': f"{p['name']} {w}g",
                'price': price,
                'desc': 'Classic vegetarian pickles made with fresh ingredients.',
                'type': 'Pickles',
                'veg': True,
                'stock': 20,
                'category': 'veg_pickles',
                'weight': w
            })
    return render_template('veg_pickles.html', products=veg_products, category='veg_pickles')

@app.route('/non-veg-pickles')
def non_veg_pickles():
    non_veg_products = []
    for p in products_fallback['non_veg_pickles']:
        if '500' in p['weights']:
            price = p['weights']['500']
            w = '500'
            non_veg_products.append({
                'id': int(f"{p['id']}{w}"),
                'base_id': p['id'],
                'name': f"{p['name']} {w}g",
                'price': price,
                'desc': 'Authentic homemade non-veg pickles, rich in flavor and tradition.',
                'type': 'Pickles',
                'veg': False,
                'stock': 20,
                'category': 'non_veg_pickles',
                'weight': w
            })
    return render_template('non_veg_pickles.html', products=non_veg_products, category='non_veg_pickles')

@app.route('/products')
def products():
    all_products = []
    for cat in ['non_veg_pickles', 'veg_pickles', 'snacks']:
        for p in products_fallback[cat]:
            if '500' in p['weights']:
                price = p['weights']['500']
                w = '500'
                all_products.append({
                    'id': int(f"{p['id']}{w}"),
                    'base_id': p['id'],
                    'name': f"{p['name']} {w}g",
                    'price': price,
                    'desc': 'Authentic homemade pickles and snacks.' if cat != 'snacks' else 'Crispy, crunchy, and delicious snacks for every occasion.',
                    'type': 'Pickles' if cat != 'snacks' else 'Snacks',
                    'veg': cat == 'veg_pickles' or cat == 'snacks',
                    'stock': 20,
                    'category': cat,
                    'weight': w
                })
    return render_template('products.html', products=all_products)

@app.route('/chicken-pickle')
def chicken_pickle():
    return render_template('chicken.html')

@app.route('/mutton-pickle')
def mutton_pickle():
    return render_template('mutton.html')

@app.route('/fish-pickle')
def fish_pickle():
    return render_template('fish.html')
  

@app.route('/veg-pickles/mango')
def mango_pickle():
    return render_template('mango.html')

@app.route('/veg-pickles/lemon')
def lemon_pickle():
    return render_template('lemon.html')

@app.route('/veg-pickles/carrot')
def carrot_pickle():
    return render_template('carrot.html')
@app.route('/order/<pickle_name>')
def order(pickle_name):
    return render_template('order.html', pickle_name=pickle_name)

@app.route('/submit-order', methods=['POST'])
def submit_order():
    name = request.form.get('name')
    phone = request.form.get('phone')
    quantity = request.form.get('quantity')
    pickle_name = request.form.get('pickle_name')

    # Here you can add logic to save to database or session

    return render_template('order_confirmation.html', name=name, phone=phone, quantity=quantity, pickle_name=pickle_name)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        users = load_users()
        if any(u['username'] == username for u in users):
            return render_template('signup.html', error="User already exists!")
        users.append({'username': username, 'password': password})
        save_users(users)
        flash("Signup successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        users = load_users()
        if any(u['username'] == username and u['password'] == password for u in users):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials!")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('about'))

# --- Product Data Structure (for local fallback) ---
products_fallback = {
    'non_veg_pickles': [
        {'id': 1, 'name': 'Non-Veg Chicken Pickle', 'weights': {'250': 600, '500': 1200, '1000': 1800}},
        {'id': 2, 'name': 'Non-Veg Fish Pickle', 'weights': {'250': 200, '500': 400, '1000': 800}},
        {'id': 3, 'name': 'Non-Veg Gongura Mutton Pickle', 'weights': {'250': 400, '500': 800, '1000': 1600}},
        {'id': 4, 'name': 'Non-Veg Mutton Pickle', 'weights': {'250': 400, '500': 800, '1000': 1600}},
        {'id': 5, 'name': 'Non-Veg Prawns Pickle', 'weights': {'250': 600, '500': 1200, '1000': 1800}},
        {'id': 6, 'name': 'Non-Veg Gongura Chicken Pickle', 'weights': {'250': 350, '500': 700, '1000': 1050}},
    ],
    'veg_pickles': [
        {'id': 7, 'name': 'Veg Mango Pickle', 'weights': {'250': 150, '500': 280, '1000': 500}},
        {'id': 8, 'name': 'Veg Lemon Pickle', 'weights': {'250': 120, '500': 220, '1000': 400}},
        {'id': 9, 'name': 'Veg Tomato Pickle', 'weights': {'250': 130, '500': 240, '1000': 450}},
        {'id': 10, 'name': 'Veg Mix Pickle', 'weights': {'250': 130, '500': 240, '1000': 450}},
        {'id': 12, 'name': 'Veg Spicy Pandu Mirchi Pickle', 'weights': {'250': 130, '500': 240, '1000': 450}},
    ],
    'snacks': [
        {'id': 13, 'name': 'Snacks Banana Chips', 'weights': {'250': 300, '500': 600, '1000': 800}},
        {'id': 14, 'name': 'Snacks Crispy Aam-Papad', 'weights': {'250': 150, '500': 300, '1000': 600}},
        {'id': 16, 'name': 'Snacks Sweet Boondhi', 'weights': {'250': 300, '500': 600, '1000': 900}},
        {'id': 17, 'name': 'Snacks Chekkalu', 'weights': {'250': 350, '500': 700, '1000': 1000}},
        {'id': 18, 'name': 'Snacks Ragi Laddu', 'weights': {'250': 350, '500': 700, '1000': 1000}},
        {'id': 19, 'name': 'Snacks Dry Fruit Laddu', 'weights': {'250': 500, '500': 1000, '1000': 1500}},
        {'id': 20, 'name': 'Snacks Kara Boondi', 'weights': {'250': 250, '500': 500, '1000': 750}},
        {'id': 21, 'name': 'Snacks Gavvalu', 'weights': {'250': 250, '500': 500, '1000': 750}},
    ]
}

# ---------- MAIN ----------

if __name__ == '__main__':
    app.run(debug=True)