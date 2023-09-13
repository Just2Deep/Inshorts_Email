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


now = datetime.datetime.now()

# email placeholder

BASE_URL = "https://www.inshorts.com/en/read"
CONTENT_LINK_URL = "https://inshorts.com"
FROM = ""  # email address of the sender
TO = ""  # email address of the receiver
PASS = "-----------"  #

content = ""

# Extracting News Stories


def scrape_html(url: str) -> str:
    content = requests.get(url).content

    return BeautifulSoup(content, "html.parser")


def fetch_required_data(soup: BeautifulSoup, element: str, attrs: dict[str]):
    return soup.find_all(element, attrs=attrs)


def extract_news(url: str) -> str:
    """Extract News Stories

    Args:
        url (str): url for website to fetch news

    Returns:
        str: returns the content in HTML format
    """
    print("Extracting stories from Inshorts")
    cnt = ""
    cnt += "<b>Inshorts Top Stories :</b>\n" + "<br>" + "-" * 80 + "<br><br>"

    soup = scrape_html(url)
    article_title = fetch_required_data(
        soup, element="span", attrs={"itemprop": "headline"}
    )
    article_body = fetch_required_data(
        soup, element="div", attrs={"itemprop": "articleBody"}
    )
    article_link = fetch_required_data(
        soup, element="span", attrs={"itemprop": "mainEntityOfPage"}
    )

    for title, body, link in zip(article_title, article_body, article_link):
        cnt += (
            (
                "<b>"
                + title.text
                + "</b>"
                + " : "
                + "<br><br>"
                + body.text
                + "\n"
                + "<br><br>"
                + f"<a href={link.get('itemid')}"
                + "> Read more </a>"
                + "<br><br>"
                + "\n"
            )
            if body.text != "Load More"
            else ""
        )

    # we are using zip to iterate through 3 iterators and storm a string as content with title, body and actual link for news site
    return cnt


def compose_html_for_mail(content: str) -> str:
    content += "<br>------------------------------------------------------------------------------<br>"
    # content += ('<br><br>End of Message<br><br>')
    content += "Made with <3, Deep :)<br>"
    content += "Thanks for reading!"

    return content


def send_the_mail(content):
    # Email Deatils

    SERVER = "smtp.gmail.com"  # your smtp server
    PORT = 587  # your port number

    # password.(since the changes from google for less secure apps, we can use app password for this)

    # create text/plain message
    msg = MIMEText("")

    msg = MIMEMultipart()

    # creating a dynamic subject for the email
    msg[
        "Subject"
    ] = f"Top Stories from Inshorts. [Automated Email] {now.strftime('%d %b %Y')}"

    msg["From"] = FROM
    msg["To"] = TO

    msg.attach(MIMEText(content, "html"))

    print("Initiating Server....")

    server = smtplib.SMTP(SERVER, PORT)
    server.set_debuglevel(1)  # to check errors
    server.ehlo()
    server.starttls()
    server.login(FROM, PASS)
    server.sendmail(FROM, TO, msg.as_string())

    print("Email Sent...")

    server.quit()


if __name__ == "__main__":
    content = extract_news(BASE_URL)
    final_content = compose_html_for_mail(content)
