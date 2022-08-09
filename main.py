# Webscraping and automation

import requests  # http requests
# Send the mail
import smtplib
from bs4 import BeautifulSoup  # web scraping
# email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# system date and time
import datetime
# string matching
import re

now = datetime.datetime.now()

# email placeholder

content = ''

# Extracting News Stories


def extract_news(url):
    print('Extracting stories from Inshorts')
    cnt = ''
    cnt += ('<b>Inshorts Top Stories :</b>\n' + '<br>' + '-'*80 + '<br><br>')
    response = requests.get(url)
    content = response.content

    soup = BeautifulSoup(content, 'html.parser')
    for title, body, link in zip(soup.find_all('span', attrs={'itemprop': 'headline'}), (soup.find_all('div', attrs={'itemprop': 'articleBody'})), soup.find_all('a', attrs={'href': re.compile("^/en/news/")})):
        cnt += ('<b>'+title.text+'</b>' + ' : ' + '<br><br>' + body.text + "\n" + '<br><br>' + '<a href=https://inshorts.com' +
                link.get('href') + '> Read more </a>' + '<br><br>' + "\n") if body.text != 'Load More' else ''

    # we are using zip to iterate through 3 iterators and storm a string as content with title, body and actual link for news site
    return (cnt)


cnt = extract_news('https://www.inshorts.com/en/read')

content += cnt
content += ('<br>-------------------------------------------------------------------------------<br>')
# content += ('<br><br>End of Message<br><br>')
content += ('Made with <3, Deep :)<br>')
content += ('Thanks for reading!')

# print(content)

# Sending the email.

print('Composing Email.')

# Email Deatils

SERVER = 'smtp.gmail.com'  # your smtp server
PORT = 587  # your port number
FROM = '--------'  # from email
TO = '---------'  # to email id
# password.(since the changes from google for less secure apps, we can use app password for this)
PASS = '-----------'


# create text/plain message
msg = MIMEText('')

msg = MIMEMultipart()

# creating a dynamic subject for the email
msg['Subject'] = 'Top Stories from Inshorts. [Automated Email] ' + \
    str(now.day) + '/' + str(now.month) + '/' + str(now.year)

msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))


print('Initiating Server....')

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)  # to check errors
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()
