import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email account credentials
sender_email = "ibcs83293@gmail.com"
sender_password = "kvqo oydg pzxc afow"
receiver_email = "yandabaodav@gmail.com"

# Email content
subject = "Test Email from Python"
body = "This is a test email sent from a Python script."

# Create a MIME object
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

# Attach the body with the msg instance
msg.attach(MIMEText(body, 'plain'))

try:
    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Secure the connection
    server.login(sender_email, sender_password)
    
    # Send the email
    server.sendmail(sender_email, receiver_email, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Terminate the SMTP session
    server.quit()