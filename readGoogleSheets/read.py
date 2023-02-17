import os.path
import requests

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from os import environ, path
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
import re
import csv
import time
from smtplib import SMTPAuthenticationError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

SECRET_P = environ.get('PASS')

SAMPLE_SPREADSHEET_ID = '' #Master Spreadsheet id
SAMPLE_RANGE_NAME = 'Master List!A2:A266'

clientemailist = []

instagramlist = []

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

def isValid(email):
    if re.fullmatch(regex, email):
        clientemailist.append(email)

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    if os.path.exists('credentials.json'): #full path for your credentials file
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json') #full path for your credentials file

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        # Fill in emails array with sheet and column data from your google sheet
        sheet = service.spreadsheets()
        print(sheet)
        emails = [sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='France!B2:B67').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='England!B2:B29').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Germany!B2:B52').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Scotland!B2:B7').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Ibiza!A2:A26').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Holland!A2:A18').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Switzerland!A2:A22').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Spain!B2:B48').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Monte Carlo!A2:A6').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Portugal!A2:A15').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Italy!A2:A37').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Norway!A2:A7').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Sweden!B2:A11').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Belgium!B2:B16').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Austria!B2:B6').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Poland!A2:A5').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Bosnia!A2:A2').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Luxemburg!B2:B2').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Denmark!A2:A7').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Czech Republic!A2:A7').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Croatia!A2:A13').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Montenegro!A2:A6').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Hungray!A2:A4').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Serbia!A2:A17').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Bulgaria!A2:A3').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Ireland!E2:E2').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Slovakia!A2:A4').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Greece!A2:A26').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Romania!A2:A6').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Estonia!A2:A6').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Ukraine!A2:A12').execute()
        ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Russia!A2:A5').execute()]

        for e in emails:
            values = e.get('values',[])

            if not values:
                print('No data found.')

            elif values:
                for row in values:
                    for each in row:
                        isValid(each)

        fields = ['Email address']
        filename = "leademail.csv"
        with open(filename, 'w') as fileObj:
            writerObj = csv.writer(fileObj)
            # Add header row as the list
            writerObj.writerow(fields)

            for c in set(clientemailist):
                writerObj.writerow([c])

        service = build("sheets", "v4", credentials=creds)  # Please use your script for authorization.
        spreadsheet_id = ""  # Please put your Spreadsheet ID.
        sheet_name = "emails"  # Please put the sheet ID of the sheet you want to use.
        csv_file = "leademail.csv"  # Please put the file path of the CSV file you want to use.

        f = open(csv_file, "r")
        values = list(filter(None,[r for r in csv.reader(f)]))
        service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=sheet_name, valueInputOption='USER_ENTERED', body={"values": values}).execute()

        writeEmails()

    except HttpError as err:
        print(err)

    else:
        pass


            
def writeEmails():

    if os.path.exists('leademail.csv'): #full path of the leademail.csv, should be at root of projects
        try:
            username = ''  # Email Address from the email you want to send an email
            password = SECRET_P  # Password
            # Create the body of the message (a HTML version for formatting).
            html = """
            <!DOCTYPE html>
            <html>
                    <body>
                        <div style="font-family: Arial">
                            <h2 style=style="font-family: Arial">My newsletter</h2>
                        </div>
                        <div style="padding:20px 0px">
                            <div style="height: 500px;width:400px">
                                <img src="https://images.unsplash.com/photo-1544785316-6e58aed68a50?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=400&q=80" style="height: 300px;">
                                <div style="text-align:center;">
                                    <h3>Article 1</h3>
                                    <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. A ducimus deleniti nemo quibusdam iste sint!</p>
                                    <a href="#">Read more</a>
                                </div>
                            </div>
                        </div>
                    </body>
                </html>
            """

            emlist = open('leademail2.csv', 'r')
            values2 = [r for r in csv.reader(emlist)]
            
            for v in [element for sublist in values2[1:] for element in sublist]:
                msg = MIMEMultipart()
                msg['Subject'] = "function test"
                msg['From'] = username
                msg['To'] = v
                print(v)

                # Attach HTML to the email
                body = MIMEText(html, 'html')
                msg.attach(body)
                print(msg)
                time.sleep(1)
                
                try:

                    context = ssl.create_default_context()

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(username, password)
                        smtp.sendmail(username, v, msg.as_string())
                except SMTPAuthenticationError:
                    print('SMTPAuthenticationError')
                    print("Email not sent to", v)

        except HttpError as err:
            print(err)
    else:
        main()

def insta():

        if os.path.exists('credentials.json'):
            creds = None
            creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json')
        try:
            service = build('sheets', 'v4', credentials=creds)
            # Call the Sheets API
            # Fill in usernames array with sheet and column data from your google sheet
            sheet = service.spreadsheets()
            print(sheet)
            usernames = [ sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='France!D2:D67').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='England!D2:D36').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Germany!D2:D52').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Scotland!E2:E7').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Ibiza!E2:E26').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Holland!G2:G18').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Switzerland!E2:E22').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Spain!D2:D48').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Monte Carlo!E2:E6').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Portugal!G2:G15').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Italy!F2:F37').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Norway!F2:F7').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Sweden!D2:D11').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Belgium!D2:D16').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Austria!D2:D6').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Poland!G2:G5').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Bosnia!E2:E2').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Latvia!E2:E6').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Luxemburg!D2:D5').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Denmark!E2:E7').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Czech Republic!D2:D8').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Croatia!D2:D13').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Montenegro!F2:F6').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Hungray!D2:D4').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Serbia!G2:G17').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Bulgaria!E2:E3').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Ireland!F2:F4').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Slovakia!E2:E4').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Greece!D2:D35').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Cyprus!D2:D2').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Romania!F2:F6').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Estonia!E2:E6').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Ukraine!F2:F12').execute()
            ,sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Russia!F2:F5').execute()]

            for u in usernames:
                values = u.get('values',[])

                if not values:
                    print('No data found.')
                elif values:
                    for v in values:
                        for grams in v:
                            instagramlist.append(grams)

            fields = ['usernames']
            filename = "instagram.csv"
            with open(filename, 'w') as fileObj:
                writerObj = csv.writer(fileObj)
                # Add header row as the list
                writerObj.writerow(fields)

                for gr in set(instagramlist):
                    us = gr.replace(' ', '')
                    writerObj.writerow([us])

            service = build("sheets", "v4", credentials=creds)  # Please use your script for authorization.
            spreadsheet_id = ""  # Please put your Spreadsheet ID.
            sheet_name = "usernames"  # Please put the sheet ID of the sheet you want to use.
            csv_file = "instagram.csv"  # Please put the file path of the CSV file you want to use.

            try:
                f = open(csv_file, "r")
                values = list(filter(None,[r for r in csv.reader(f)]))
                service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=sheet_name, valueInputOption='USER_ENTERED', body={"values": values}).execute()
            except:
                print('invalid file')

        except HttpError as err:
            print(err)

        else:
            pass

def updateInsta():
    if os.path.exists('instagram.csv'):
        pass
    else:
        insta()

if __name__ == '__main__':
    writeEmails()
    updateInsta() #the logic of the updateInsta() and insta() function are discrectionary to the developer