# Pylio
Send email messages through a specified Gmail account.

## Getting Started
1) Download Pylio and its dependancies 
`pip install pylio`

2) Turn on Gmail API by clicking **Enable Gmail API** on [Gmail](gmailAPIon)
    1) Select **+ Create a new project**.
    2) Download the credentials file to access your Gmail account. 
    3) Move the downloaded file to your working directory and ensure it is named `credentials.json`. \
       You can also specify the location of `credentials.json` either in `config.yaml` or using the `--cred-file` flag.
       
3) From command line: use `pylio` with the below arguments. Default arguments will come from the `config.yaml` unless otherwise stated. <br>       
Command line override arguments: <br>
  `--to email_address` email address of intented recepient \
  `--message msg_body` text body of email \
  `--config-file path` (optional) path to custom configuration file; default is `config.yaml` \
  `--cred-file path` (optional) path to Google Gmail credentials JSON file \
  `--subject subject_line` (optional) subject line of email 


## Contents
`config.yaml` Default configuration file to specify to, message, and Google credentials file \
`PylioMail.py` Class using Google API \
`setup.py` pip file

## How does it work? 
This repository is a wrapper that simplifies the use of the [Google Gmail API](gmailAPI).  

## Troubleshooting
- Check if authorization is enabled: [Google Authorization](https://developers.google.com/gmail/api/auth/about-auth)
- Make sure `https://www.googleapis.com/auth/gmail.send` is chosen in [authorization](https://developers.google.com/gmail/api/auth/web-server).

2018 (c) Xavier Collantes

[gmailAPI]:("https://developers.google.com/gmail/api/")
[gmailAPIon]:("https://developers.google.com/gmail/api/quickstart/python")
