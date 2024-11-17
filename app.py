from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import newsapi
import requests
import smtplib
import schedule
import time
from requirements import STOCK_NAME , COMPANY_NAME , api_key_alphavantage , api_key_news , my_email , password
# Your existing constants
# STOCK_NAME = "TSLA"
# COMPANY_NAME = "Tesla Inc"
# api_key_alphavantage = "POFBA2EN11KWWTA7"
# api_key_news = "8f3ba393bf1e4bd3a9dca8cd66082fd4"
# my_email = "www.nishantwailkar71@gmail.com"
# password = "jmav jpxr suvi tmlw"

# Setup Flask app
app = Flask(__name__)

# Database setup - Create DB and table if not exist (done once)
def setup_db():
    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            stock TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Add user to the database
def add_user(email, stock):
    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, stock) VALUES (?, ?)", (email, stock))
    conn.commit()
    conn.close()

# Get all users from the database
def get_users():
    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email, stock FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

# Home route (index page with form)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    stock = request.form['stock']
    add_user(email, stock)
    return redirect(url_for('index'))

# Function to send email updates based on stock price
def send_emails():
    users = get_users()
    for email, stock in users:
        parameters = {
            "function": "TIME_SERIES_DAILY",
            "symbol": stock,
            "apikey": api_key_alphavantage,
        }
        response = requests.get("https://www.alphavantage.co/query", params=parameters)
        data = response.json()
        data_list = [value for key, value in data.items()]
        yesterday_closing_price = float(data_list[0]['4. close'])
        day_before_yesterday_closing_price = float(data_list[1]['4. close'])
        difference = abs(yesterday_closing_price - day_before_yesterday_closing_price)
        percent_diff = (difference / yesterday_closing_price) * 100
        percent_diff_formatted = round(percent_diff, 2)

        if percent_diff > 5:
            news_params = {
                'q': stock,
                'apiKey': api_key_news
            }
            response2 = requests.get(url="https://newsapi.org/v2/everything", params=news_params)
            response2.raise_for_status()
            articles = response2.json()['articles']
            three_articles = articles[:3]
            new_list_articles = [
                f"Headline: {article['title']}. \n Brief: {article['description']} See More Here: {article['url']}"
                for article in three_articles
            ]
            if yesterday_closing_price > day_before_yesterday_closing_price:
                arrow = "🔺"
            else:
                arrow = "🔻"
            msg = f"Subject: {stock} {arrow}{percent_diff_formatted}%\n\n"
            for article in new_list_articles:
                msg += f"{article}\n\n"
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=email,
                    msg=msg.encode('utf-8')
                )

# Schedule the email sending task to run daily at 9:00 AM
schedule.every().day.at("09:00").do(send_emails)

# Run the scheduled tasks
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

# Run the scheduler in a separate thread
import threading
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

if __name__ == '__main__':
    setup_db()  # Ensure the DB is set up when app starts
    app.run(debug=True, use_reloader=False)  # use_reloader=False to avoid multiple scheduler threads
