from flask_mail import Message
from .mail_flask import mail
from jinja2 import Environment, FileSystemLoader


# general function to either send mails to admin or the users 
def sendMail(RECEIVER_ADDRESS,SUBJECT,MESSAGE,ATTACHMENT=None,mime_type = "application/pdf", booking_data=None):


    try:
       
        msg = Message(recipients=[RECEIVER_ADDRESS],
                    sender='gsoni.2301@gmail.com',
                    body=MESSAGE,
                    subject=SUBJECT)

        if ATTACHMENT :
            
            with open(ATTACHMENT, 'rb') as fp:
                if mime_type == "application/pdf" :
                    msg.attach(f"{RECEIVER_ADDRESS}_report.pdf",mime_type , fp.read())
                elif mime_type == "application/x-zip" :
                    msg.attach(f"{RECEIVER_ADDRESS}_exported.zip",mime_type , fp.read())
                elif mime_type == "text/csv":  # Add this block for .csv files
                    msg.attach(f"{RECEIVER_ADDRESS}_data.csv", mime_type, fp.read())

        if booking_data:
            # Load the Jinja2 environment
            env = Environment(loader=FileSystemLoader('./Backend/templates'))  # Replace with your actual template directory

            # Load the HTML template
            template = env.get_template('report.html')  # Replace with your actual template file

            # Render the template with data
            rendered_html = template.render(bookings=booking_data)
            msg.html = rendered_html  # Set the HTML content of the email


        mail.send(msg)
        return True

    except Exception as e:
        print(e)
        return False
