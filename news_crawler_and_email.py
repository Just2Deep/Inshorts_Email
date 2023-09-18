# Webscraping and automation

# system date and time
import datetime
import os

import requests  # http requests
import smtplib
from bs4 import BeautifulSoup  # web scraping
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import dotenv_values


now = datetime.datetime.now()

# email placeholder

config = {**dotenv_values("sample.env"), **dotenv_values(".env"), **os.environ}

BASE_URL = "https://www.inshorts.com/en/read"
CONTENT_LINK_URL = "https://inshorts.com"
FROM = config["FROM"]  # email address of the sender
TO = config["TO"]  # email address of the receiver
PASS = config["PASS"]


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
    cnt = "<h1>Inshorts Top Stories</h1>"

    soup = scrape_html(url)
    title_attrs = {"itemprop": "headline"}
    body_attrs = {"itemprop": "articleBody"}
    link_attrs = {"itemprop": "mainEntityOfPage"}

    article_title = fetch_required_data(soup, element="span", attrs=title_attrs)
    article_body = fetch_required_data(soup, element="div", attrs=body_attrs)
    article_link = fetch_required_data(soup, element="span", attrs=link_attrs)

    for title, body, link in zip(article_title, article_body, article_link):
        cnt += (
            (
                "<h2>"
                + title.text
                + "</h2>"
                + f"<p>{body.text}</p>"
                + f"<button><a href={link.get('itemid')}> Read more </a></button>"
            )
            if body.text != "Load More"
            else ""
        )

    # we are using zip to iterate through 3 iterators and storm a string as content with title, body and actual link for news site
    return cnt


def compose_html_for_mail(content: str) -> str:
    content += "<p>Made with <3, Thanks for reading!</p>"
    content += "<p>Regards,<br>Deep :)</p>"

    return content


def send_the_mail(content: str):
    # Email Deatils

    SERVER = "smtp.gmail.com"  # your smtp server
    PORT = 587  # your port number

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
    # server.set_debuglevel(1)  # to check messages and errors
    server.ehlo()
    server.starttls()
    server.login(FROM, PASS)
    server.sendmail(FROM, TO, msg.as_string())

    print("Email Sent...")

    server.quit()


if __name__ == "__main__":
    content = extract_news(BASE_URL)
    final_content = compose_html_for_mail(content)
    send_the_mail(final_content)
