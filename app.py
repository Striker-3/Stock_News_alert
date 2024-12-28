from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import newsapi
import requests
import smtplib
import schedule
import time
import os
from dotenv import load_dotenv
import threading


app = Flask(__name__)

# adding env variables
load_dotenv()
api_key_alphavantage = os.getenv("API_KEY_ALPHAVANTAGE")
api_key_news = os.getenv("API_KEY_NEWS")
my_email = os.getenv("SENDERS_EMAIL")
password = os.getenv("PASSWORD")
stock_api = os.getenv("API_KEY_STOCKS_FINANCIALMODELLING")


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


def add_user(email, stock):
    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, stock) VALUES (?, ?)", (email, stock))
    conn.commit()
    conn.close()


def get_users():
    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email, stock FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


def get_stock_data(stock_symbol):
    response1 = requests.get(
        f"https://financialmodelingprep.com/api/v3/search?query={stock_symbol}&apikey=HemPBSRpXfBTAoIe9jojlPUSJWKkPGTB")
    data1 = response1.json()
    return data1


# for input suggestins
@app.route('/api/search_stocks')
def search_stocks():
    query = request.args.get('query', '')
    if not query:
        return {"stocks": []}
    try:
        response = requests.get(
            f"https://financialmodelingprep.com/api/v3/search?query={query}&limit=10&apikey=HemPBSRpXfBTAoIe9jojlPUSJWKkPGTB"
        )
        response.raise_for_status()
        data = response.json()
        stocks = [{"symbol": stock["symbol"], "name": stock["name"]} for stock in data]
        return {"stocks": stocks}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    stock = request.form['stock']
    add_user(email, stock)

    stock_data = get_stock_data(stock)

    if "error" in stock_data:
        return "Error"

    if stock_data and isinstance(stock_data, list) and len(stock_data) > 0:
        stock_symbol = stock_data[0].get('symbol')
        stock_name = stock_data[0].get('name')
    else:
        return "Invalid stock data received."

    return render_template('confirmation.html', stock=stock, stock_symbol=stock_symbol, stock_name=stock_name)


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


schedule.every().day.at("09:00").do(send_emails)


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)


scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# if __name__ == '__main__':
#     setup_db()
#     app.run(debug=True, use_reloader=False)
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

