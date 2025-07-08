from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
app.secret_key = os.urandom(24)

# AWS Configuration
region = 'ap-south-1'
dynamodb = boto3.resource('dynamodb', region_name=region)
sns = boto3.client('sns', region_name=region)

# AWS Resources
users_table = dynamodb.Table('Users')
orders_table = dynamodb.Table('Orders')
SNS_TOPIC_ARN = 'arn:aws:sns:ap-south-1:your-account-id:OrderNotifications'

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login', next=request.url))
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            response = users_table.get_item(Key={'username': username})
            user = response.get('Item')
            if user and user['password'] == password:
                session['username'] = username
                return redirect('/home')
            else:
                return render_template('login.html', error='Invalid credentials')
        except ClientError:
            return render_template('login.html', error='Login error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            users_table.put_item(Item={'username': username, 'password': password})
            return redirect('/login')
        except ClientError:
            return render_template('signup.html', error='Signup failed.')
    return render_template('signup.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful', 'loggedIn': False}), 200

@app.route('/check-auth', methods=['GET'])
def check_auth_status():
    return jsonify({'loggedIn': 'username' in session}), 200

@app.route('/user-data', methods=['GET'])
def get_user_data():
    if 'username' in session:
        return jsonify({'username': session.get('username')}), 200
    return jsonify({'message': 'Not logged in'}), 401

@app.route('/account')
def account_page():
    if 'username' not in session:
        return redirect(url_for('login', next=request.url))
    return render_template('account.html')

@app.route('/checkout')
def checkout_page():
    if 'username' not in session:
        return redirect(url_for('login', next=request.url))
    return render_template('checkout.html')

@app.route('/about-us')
def about_us():
    return render_template('about-us.html')

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/veg_pickles')
def veg_pickles():
    return render_template('veg-pickles.html')

@app.route('/non_veg_pickles')
def non_veg_pickles():
    return render_template('non-veg-pickles.html')

@app.route('/snacks')
def snacks():
    return render_template('snacks.html')

@app.route('/order_confirmation', methods=['GET', 'POST'])
def order_confirmation():
    if request.method == 'POST':
        order_data = request.get_json()
        print("Received order:", order_data)

        try:
            orders_table.put_item(Item=order_data)
        except ClientError as e:
            print("DynamoDB Error:", e)

        try:
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=f"New order placed: {order_data}",
                Subject='New Order Notification'
            )
        except ClientError as e:
            print("SNS Error:", e)

        return jsonify({'status': 'success'})

    return render_template('order-confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)
