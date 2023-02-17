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

Sheets id can be found in the url of a google sheet.

html in the `writeEmails()` function can be edited for whatever you want.

consider this code snippet to edit the `msg['Subject'] = "function test"`

use mailtrap.io to test sending emails from a list of real email addresses. if not
test this with your personal email addresses.

```
import random

greeting = ['Hello', 'Sup', 'Howdy', 'Hi', 'Hola', 'Greetings', 'Another word from']
random.choice(greeting) + ' company name'
```
#### program runs with
```
python3 readGoogleSheets/read.py
```
