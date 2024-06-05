import smtplib
from envVars import app_password
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email account credentials
sender_email = "ibcs83293@gmail.com"
sender_password = app_password
receiver_email = "yandabaodav@gmail.com"

def send_email_alert(receiver_email, vision_target):
    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        
        # Email content
        subject = "Vision Target Detected"
        body = "A " + vision_target + " (your target) has been detected! Here is a photo:"

        # Create a MIME object
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))
        
        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Terminate the SMTP session
        server.quit()