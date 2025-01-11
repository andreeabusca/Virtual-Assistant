

import datetime
from speak import speak

def gettime():
    time_now = datetime.datetime.now().strftime('%I:%M %p')
    speak(f"The current time is {time_now}")
    print(f"The current time is {time_now}")

def getdate():
    today = datetime.datetime.now().strftime('%B %d, %Y')
    speak(f"Today's date is {today}")
    print(f"Today's date is {today}")

    