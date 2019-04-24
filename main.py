"""
    BASIC ALGORITHM
    - Download HTML
    - Start scanning for user selected formats under English or Hindi
    - If found, send email
    - Do above steps every x minutes
"""

from urllib.request import Request, urlopen
import os
import smtplib
from email.message import EmailMessage
from apscheduler.schedulers.blocking import BlockingScheduler


def select_format(content):
    all_formats = ["2D", "3D", "IMAX 2D", "IMAX 3D", "2D 4DX", "3D 4DX", "MX4D"]
    available = []
    for i in all_formats:
        if i in content:
            available.append(i)

    print("\nSelect the format:")
    for i in range(0, len(available)):
        print(str(i + 1) + ". " + str(available[i]))
    choice = int(input("\nEnter the option number to select the format\n... "))
    return available[choice - 1]


def select_lang():
    print("Select the language:\n1. English\n2. Hindi\n")
    choice = int(input("Enter the option number to select the language\n... "))
    if choice == 1:
        return "English"
    elif choice == 2:
        return "Hindi"


def sendmail(lookup, lang, link, movie):  # If found, send email
    # insert your email id and app password instead
    email = os.environ.get('EMAIL_ID')
    app_pass = os.environ.get('BMS_PASS')

    msg = EmailMessage()
    msg['Subject'] = "BMS Notifier - " + str(movie)
    msg['From'] = email
    msg['To'] = email

    msg.set_content(
        str(lookup) + " option is now available for " + str(movie) + " in " + str(lang + "!\n\n" + str(link)))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:  # Change SMTP server name to other Email service provider's server (Yahoo, Outlook,etc.)
        smtp.send_message(msg)


def loop(url, movie, sched):
    # Download HTML (as text)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = urlopen(req).read()
    file_name = str(movie) + "- BMS.txt"
    with open(file_name, 'wb') as f:
        f.write(data)

    # Start scanning for lookup in available formats under lang
    start, end = '', ''
    lang = select_lang()

    if lang == "English":
        start = '<div id="lang-English" class="format-container">'.encode('utf-8')
        end = '<div id="lang-Hindi" class="format-container">'.encode('utf-8')
    elif lang == "Hindi":
        start = '<div id="lang-Hindi" class="format-container">'.encode('utf-8')
        end = '</body>'
    with open(file_name, 'rb') as f:
        line = f.read()
        line = line[line.find(start):line.find(end)]
        line = str(line)
        movie_format = select_format(line)
        print("Checking after every 15 minutes for " + str(movie_format) + ".")

        if movie_format in line:
            print("Found " + str(movie_format) + "!!!")
            sendmail(movie_format, lang, url, movie)
            try:
                sched.shutdown()
            except:
                print("Option now available!\n" + str(url))
                exit()
        else:
            pass


link = input("Paste link here... ")  # Eg: https://in.bookmyshow.com/mumbai/movies/avengers-endgame/ET00090482
movie_name = link[link.find('movies/'):link.find('/ET')]  # to get the movie name
movie_name = movie_name[7:]  # To remove movies/ before the name
check_period = int(input("Check after every _ minutes: "))

sched = BlockingScheduler()
loop(link, movie_name, sched)
sched.add_job(loop, 'interval', minutes=check_period, id='my_job_id', args=(link, movie_name, sched,))
sched.start()
