# https://github.com/dbader/schedule
# https://schedule.readthedocs.io/en/stable/

import schedule
import time

def job():
    print("I'm working...")

# Run job every 3 second/minute/hour/day/week,
# Starting 3 second/minute/hour/day/week from now
schedule.every(3).seconds.do(job)
schedule.every(3).minutes.do(job)
schedule.every(3).hours.do(job)
schedule.every(3).days.do(job)
schedule.every(3).weeks.do(job)

# Run job every minute at the 23rd second
schedule.every().minute.at(":23").do(job)

# Run job every hour at the 42nd minute
schedule.every().hour.at(":42").do(job)

# Run jobs every 5th hour, 20 minutes and 30 seconds in.
# If current time is 02:00, first execution is at 06:20:30
schedule.every(5).hours.at("20:30").do(job)

# Run job every day at specific HH:MM and next HH:MM:SS
schedule.every().day.at("10:30").do(job)
schedule.every().day.at("10:30:42").do(job)
schedule.every().day.at("12:42", "Europe/Amsterdam").do(job)

# Run job on a specific day of the week
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)
schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)



# Run a job once
import schedule
import time

def job_that_executes_once():
    # Do some work that only needs to happen once...
    return schedule.CancelJob

schedule.every().day.at('22:30').do(job_that_executes_once)

while True:
    schedule.run_pending()
    time.sleep(1)