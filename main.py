import newsapi
import requests

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

api_key_alphavantage = "POFBA2EN11KWWTA7"
api_key_news = "8f3ba393bf1e4bd3a9dca8cd66082fd4"

parameters_alphavantage = {
   "function":'TIME_SERIES_DAILY',
    "symbol":STOCK_NAME,
    "apikey":api_key_alphavantage,
}
response = requests.get(url="https://www.alphavantage.co/query" , params=parameters_alphavantage)

response.raise_for_status()
#
# data = response.json()['Time Series (Daily)']
# print(response.json())

# data_list = [value for (key , value) in data.items()]





    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
# yesterday_closing_price = data_list[0]['4. close']
# print(yesterday_closing_price)

#TODO 2. - Get the day before yesterday's closing stock price
# day_before_yesterday_closing_price = data_list[1]['4. close']
# print(day_before_yesterday_closing_price)

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
# difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
# print(difference)


#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
# percent_diff = (difference / float(yesterday_closing_price)) * 100
# print(percent_diff)

# #TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
# if percent_diff > 5:
news_params = {
        'q':"tesla",
        'apiKey':api_key_news
}

response2 = requests.get(url="https://newsapi.org/v2/everything",params=news_params)
response2.raise_for_status()
articles = response2.json()['articles']
# print(articles)

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
three_articles = articles[:3]

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

new_list_articles = [f"Headline: {article['title']}. \n Brief: {article['description']} " for article in three_articles]
print(new_list_articles)
#TODO 9. - Send each article as a separate message via Twilio.



#Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

