from twilio.rest import Client
import requests
from bs4 import BeautifulSoup as soup
import schedule
import datetime
import time


def read_website():
    """Reads the web site containing the affirmations we want to extract and puts all of them in a list named quotes"""
    request = requests.get('https://designepiclife.com/self-love-affirmations/', proxies={'http': '207.144.111.230'}).text
    page_soup = soup(request, 'lxml')
    text = [elem.text for elem in page_soup.find_all('ol')]
    delimiter = "."
    raw_quotes = text[0].split(delimiter)

    quotes = []
    for raw_quote in raw_quotes:
        quote = raw_quote.lstrip()
        quote = quote + delimiter
        quotes.append(quote)
    return quotes


def get_todays_affirmation(quotes):
    """ Uses the current date as a counting variable
    to ensure each new run of the program generates a different daily affirmation"""
    days_since_epoch = (
            datetime.datetime.utcnow()
            - datetime.datetime(1999, 1, 1)
    ).days
    position = (days_since_epoch % 555) - 208
    daily_affirmation = quotes[position]
    return daily_affirmation


def textmyself(daily_affirmation):
    """ Connects to Twilio's network using my unique Account SID and authorization token,
    then creates the actual text"""
    # Preset values:
    account_sid = 'AC0af800a30c81bf3662a6c2ca3453b197'
    auth_token = 'ee45da28dbe99d1bdc9e52d4bf85417e'

    # Call Client() and pass in the two variables:
    twilioCli = Client(account_sid, auth_token)
    twilioCli.api.account.messages.create(
        to="+15099349390",
        from_="+14159034989",
        body=daily_affirmation)


def send_myself_next_affirmation(quotes):
    """Combines the three previous functions to send the text"""
    read_website()
    get_todays_affirmation(quotes)
    textmyself(daily_affirmation)


if __name__ == '__main__':

    quotes = read_website()
    daily_affirmation = get_todays_affirmation(quotes)

    schedule.every(15).seconds.do(lambda: send_myself_next_affirmation(quotes))

    while True:
        schedule.run_pending()
        time.sleep(1)