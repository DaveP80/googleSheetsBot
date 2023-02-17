### Automated Program to upload a list of emails and instagram
### usernames to google sheets

```
virtualenv venv
source venv/bin/activate
```
```
pip3 install -r requirements.txt
```

This program makes the sheets in google drive, and then sends
emails to everyone in the list.

fill in all the `os.path.exists()` with the full path of those resources.

use the `leademail2.csv` as the test file for smtp functionality, fill in this file
with test email addresses.

Go to google console I.am to get your data/credentials.json information

fill in `readGoogleSheets/.env` with your google app security password.

Sheets id can be find in the url of a google sheet.

html in the `writeEmails()` function can be edited for whatever you want.

#### program runs with

```
python3 readGoogleSheets/read.py
```