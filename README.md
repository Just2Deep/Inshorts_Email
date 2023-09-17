# Webscraping and Sending Mail

### In this project we extract data from the Indian short news platform **Inshorts** and send out the content and link for these articles as an email automatically.

## How to setup

Create a virtual environment and activate it.

```
python -m venv venv

venv\Scripts\activate
```

Install all dependencies

```
pip install -r requirements.txt
```

#### You can add your email details as .env, to send top stories to your email.

#### Sample of the final email received.

![Alt text](images/sample.jpg?raw=true "Sample")

[![Automated web scraper](https://github.com/Just2Deep/Webscraping_and_sending_mail/actions/workflows/automation.yml/badge.svg)](https://github.com/Just2Deep/Webscraping_and_sending_mail/actions/workflows/automation.yml)
