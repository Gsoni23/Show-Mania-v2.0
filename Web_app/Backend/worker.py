from celery import Celery, Task, shared_task
from celery.schedules import crontab
from . import models
from .mail import sendMail
import csv
from datetime import date
from sqlalchemy.sql import func
from .database import db


# making celery app in flask application context
def create_celery_app(app):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
               return self.run(*args, **kwargs)

    celery_app = Celery(app.name,broker="redis://127.0.0.1:6379/1", backend="redis://127.0.0.1:6379/2",task_cls=FlaskTask,broker_connection_retry_on_startup=True, timezone = 'Asia/Kolkata')
    
    celery_app.conf.beat_schedule = {
        'send-monthly-entertainment-report': {
            'task': 'Scheduled Job',
            'schedule': crontab(day_of_month=1, hour=18, minute=0),
            # 'schedule': 120,
        },

        'daily-reminder': {
            'task': 'Daily Reminder',
            'schedule': crontab(hour=18, minute=0),
            # 'schedule': 120,
        },
    }

    celery_app.set_default()
    return celery_app

# CORE Reminder job to send daily reminder to the users for the bookings
@shared_task(name="Daily Reminder")
def send_daily_remainder_emails():
    try:
        # Get the current date
        current_date = date.today()

        # Query users who haven't made any bookings on the current day
        
        users_without_bookings = (
            db.session.query(models.User)
            .filter(~models.User.isadmin)
            .filter(~models.User.bookings.any(func.date(models.Booking.booking_date) == current_date))
            .all()
        )

        # print(users_without_bookings)

        # Send reminder emails
        for user in users_without_bookings:
            subject = "Daily Booking Reminder"
            message = f"Dear {user.name}, you haven't made any bookings today. Don't miss out!"
            sendMail(user.email, subject, message)

        return True
    except Exception as e:
        print(e)
        return False



# CORE scheduled job to send monthly entertainment report to the users telling them about their bookings
@shared_task(name="Scheduled Job")
def setup_periodic_tasks():
    
    users = models.User.query.filter_by(isadmin = False).all()

    for user in users:
        res = monthly_report(user)

    if(res): return [True,'Successfully Exported']
    else : return [False,'Failed to export']

# Export job to send the venue data to the admin
@shared_task(name="Export Job")
def export_data(venue_id):

    res = export_venue_data(venue_id=venue_id)
            
    if(res): return [True,'Successfully Exported']
    else : return [False,'Failed to export']



def export_venue_data(venue_id):
    try:
        # Get the Venues to export
        venue = models.Venue.query.get(int(venue_id))

        # Get the admin from database
        admin = models.User.query.get(int(venue.owner))

        file_path = "venue_export.csv"

        # Write the content in the file
        with open(file_path, 'w', newline='') as csv_file:
            fieldnames = ['venue_id', 'venue_name', 'place', 'capacity', 'no. of shows', 'shows'] 
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            writer.writerow({
                'venue_id': venue.venue_id, 
                'venue_name': venue.venue_name,
                'place': venue.place,
                'capacity': venue.capacity,
                'no. of shows': len(venue.shows),
                'shows': venue.shows
            })

        # Send the email to admin with the csv file in atatchment
        res = sendMail(admin.email,"Venue Exports","The venue info has been exported and attached below in CSV file format.",file_path,"text/csv")
        return res
    except Exception as e:
        print(e)
        return False


def monthly_report(user):
    try:

        # Get the bookings of the user
        bookings = models.Booking.query.filter_by(user=user.user_id).all()

        formatted_bookings_list = []
        for booking in bookings:
            show = models.Show.query.filter_by(show_id = int(booking.show)).first()
            venue = models.Venue.query.filter_by(venue_id = int(show.hall)).first()

            formatted_booking = {
                "booking_id": booking.booking_id,
                "show_name": show.show_name,
                "venue_name": venue.venue_name,
                "venue_location": venue.place,
                "start_time": show.start_time,
                "end_time": show.end_time,
                "rating": show.rating,
                "tickets": booking.tickets
            }

            formatted_bookings_list.append(formatted_booking)
        

        # Send the email to user
        res = sendMail(user.email, "Monthly Report", "The monthly report of your bookings is attached below.",booking_data = formatted_bookings_list)
        return res

    except Exception as e:
        print(e)
        return False