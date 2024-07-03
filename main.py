import newsapi
import requests
import smtplib

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

api_key_alphavantage = "POFBA2EN11KWWTA7"
api_key_news = "8f3ba393bf1e4bd3a9dca8cd66082fd4"

parameters_alphavantage = {
    "function": 'TIME_SERIES_DAILY',
    "symbol": STOCK_NAME,
    "apikey": api_key_alphavantage,
}
response = requests.get(url="https://www.alphavantage.co/query", params=parameters_alphavantage)

response.raise_for_status()

data = response.json()['Time Series (Daily)']
# print(response.json())

data_list = [value for (key, value) in data.items()]

yesterday_closing_price = data_list[0]['4. close']
# print(yesterday_closing_price)

day_before_yesterday_closing_price = data_list[1]['4. close']
# print(day_before_yesterday_closing_price)

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
# print(difference)

percent_diff = (difference / float(yesterday_closing_price)) * 100
percent_diff_formatted = round(percent_diff, 2)
# print(percent_diff_formatted)

if percent_diff > 5:
    news_params = {
        'q': "tesla",
        'apiKey': api_key_news
    }

    response2 = requests.get(url="https://newsapi.org/v2/everything", params=news_params)
    response2.raise_for_status()
    articles = response2.json()['articles']

    three_articles = articles[:3]

    new_list_articles = [f"Headline: {article['title']}. \n Brief: {article['description']} " for article in
                         three_articles]
    # print(new_list_articles)

    my_email = "www.nishantwailkar71@gmail.com"
    password = "goub ejpi fbtf pryc"
    if yesterday_closing_price > day_before_yesterday_closing_price:
        arrow = "🔺"
    else:
        arrow = "🔻"

    msg = f"Subject: TSLA {arrow}{percent_diff_formatted}\n\n"
    for article in new_list_articles:
        msg += f"{article}\n\n"

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="nishantw631@gmail.com",
            msg=msg.encode('utf-8')
        )
