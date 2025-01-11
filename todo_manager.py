
import csv
import datetime
from speak import speak

def delete_old():
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    months = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
              "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12}

    activity_list = []
    
    with open("todolist.csv", "r", newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for line in reader:
            activity_list.append(line)

    # Write back only the activities that are from the current or future months/years
    with open("todolist.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

        for activity in activity_list:
            try:
                # Ensure month is valid and handle case sensitivity
                activity_month = months[activity[4].strip().lower()]
                activity_year =  int(activity[5].strip())  

                if activity_month >= current_month and activity_year >= current_year:
                    writer.writerow(activity)
            except KeyError as e:
                print(f"Skipping invalid entry (Invalid month): {activity}, Error: {e}")
                continue  # Skip invalid months
            except ValueError as e:
                print(f"Skipping invalid entry (Invalid day or month): {activity}, Error: {e}")
                continue  # Skip invalid day or month

def add_activity(activity):
    activity_info = activity.split(",")

    activity_list = [] 
    with open("todolist.csv","r",newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            activity_list.append(line)

    with open("todolist.csv","w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(activity_list)
        writer.writerow(activity_info)
    speak("The new task was added to the list")

def get_activities():
    current_month = datetime.datetime.now().strftime('%B').lower()
    current_day = str(int(datetime.datetime.now().strftime('%d')))
    activity_list = []
    activity_today = 0
    activity_today_list = []

    print(current_day)
    print(current_month)

    with open("todolist.csv","r", newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            activity_list.append(line)

    speak("You have ")

    for activity in activity_list:
        if activity[3].strip() == current_day and activity[4].strip() == current_month:
            speak(f"{activity[0]} at {activity[2]}")
            activity_today_list.append(activity)
            activity_today = 1

    if activity_today == 0:
        speak("nothing scheduled")

    speak("today")
    
    with open("todolist.csv","w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(activity_list)
    return activity_today_list