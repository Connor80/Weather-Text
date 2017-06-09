from bs4 import BeautifulSoup
import requests
from twilio.rest import Client

# Account SID from twilio.com/console
account_sid = "ACb73022b9e8b7af5fc6627e95170bd5bd"
# Auth Token from twilio.com/console
auth_token  = "485be409b146334f96d4e9576351a6e9"

client = Client(account_sid, auth_token)

url = 'https://www.wunderground.com/us/tx/dallas'
webpage = requests.get(url)
soup = BeautifulSoup(webpage.text, 'html.parser')

# Weather sentence at top of page - not live
sentenceParse = soup.findAll("div", {"data-station":"KTXDALLA339"})
for a in sentenceParse:
    Sentence = a.string

# Time of Sunset
sunsetParse = soup.findAll("span", {"id":"cc-sun-set"})
for b in sunsetParse:
    Sunset = b.string + "pm"

# Stage and Visibility of Moon
moonParse = soup.findAll("div", {"class":"moonNorth"})
for c in moonParse:
    Moon = c.getText().strip()

# High Temperature - not live
highParse = soup.findAll("div", {"class":"small-6 columns"})
for d in highParse:
    High = d.getText()

# Low Temperature - not live
lowParse = soup.findAll("strong", {"class":"low"})
for e in highParse:
    Low = e.string

# Current Time and Date
dateParse = soup.findAll("div", {"class":"local-time"})
for f in dateParse:
    Date = f.getText()

# Body of SMS message to be sent
body = "It is" + Date + ". Sunset is at " + Sunset + " and the moon will be " + Moon + "."
#print(body)

# Generate and send SMS message. Add numbers from account.
message = client.messages.create(
    to="+1", 
    from_="+1",
    body=body)
