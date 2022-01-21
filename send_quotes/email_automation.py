import data_collection
import random
import time
import smtplib
from datetime import datetime
from email.message import EmailMessage


def send_email(list_of_quotes, first_name, to_send_to, subject='Quote of the Day'):

    """A function to choose a random quote from a big selection and send an email with that quote"""

    quote, author = random.choice(list_of_quotes)
    message_body = f'Hi {first_name.title()}!\n\nHere is the quote of the day:\n"{quote} ~ {author}"'

    email_message = EmailMessage()
    email_message.set_content(message_body)
    email_message['subject'] = subject

    user_sent_from = 'testemail999955@gmail.com'
    email_message['from'] = user_sent_from
    email_message['to'] = to_send_to

    password = 'xxtfurqclzzzithe'  # This is no longer the password because I changed it

    # Documentation found at: https://docs.python.org/3/library/smtplib.html
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()

    server.login(user_sent_from, password)
    server.send_message(email_message)

    server.quit()


if __name__ == '__main__':

    quote_choices = data_collection.get_all_quotes()

    # Relevant input to send a message at any given time
    name = input('Enter your name: ')
    year = int(input('Year: '))
    month = int(input('Month: '))
    day = int(input('Day: '))
    hour = int(input('Hour: '))
    minute = int(input('Minute: '))
    seconds = int(input('Second: '))

    print('\nPreparing to send...')

    send_time = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=seconds)
    time.sleep(send_time.timestamp() - time.time())

    send_email(quote_choices, name, 'nojorub@gmail.com')
    print(f'Email sent at {send_time}!')


