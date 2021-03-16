import requests, os
from bs4 import BeautifulSoup as bs
from twilio.rest import Client
import datetime
url = 'https://mychartweb.ohsu.edu/mychart/SignupAndSchedule/EmbeddedSchedule?view=plain&public=1&id=84586,84587,84590&dept=237170004,237160001&vt=7504'

def send_message():
    account_sid = os.getenv('TWILIO_ACCT_ID')
    auth_token = os.getenv('TWILIO_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+12148933072",
        from_="+18142564475",
        body=f"Appointment is available!  See {url}")

    print(message.sid)

if __name__ == '__main__':
    if os.getenv('TEST_FLAG'): send_message()

    resp = requests.get(url)
    bsr = bs(resp.content, 'html.parser')

    v = bsr.select_one('div[data-rsrc-id="dayName_1"]')
    if v.parent.attrs['class'] == ['hidden']: 
        print(f'{datetime.datetime.now()}: No appointments')
    else:
        send_message()

