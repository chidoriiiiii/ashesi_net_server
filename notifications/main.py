import psycopg2
from firebase_admin import credentials, firestore, initialize_app
import smtplib
import ssl
from email.mime.text import MIMEText

cred = credentials.Certificate('key.json')
initialize_app(cred)

db = firestore.client()
# conn = psycopg2.connect(
#     host="localhost",
#     database="ashesi_net",
#     user="postgres",
#     password="guuk12jona"
# )

# cur = conn.cursor()
# cur.execute('SELECT email_address FROM "user"')
# emails = [row for row in cur.fetchall()]
emails = [
    "kuugjonathan45@gmail.com",
    "jonathankuug45@gmail.com",
    "fortnitelegends19@gmail.com",
    "jxterkxg@gmail.com",
    "florencekuug81@gmail.com"]


def send_notification_email(data, context):
    print(data, context)
    notification_ref = db.collection('notification').document(context.event_id)
    lastest_notification = notification_ref.get().to_dict()
    msg = MIMEText(f"A new post with title placeholder has been created.")
    msg['Subject'] = 'New post created'
    msg['From'] = 'theashesinetwork@gmail.com'
    msg['To'] = ", ".join(emails)
    ssl_context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl_context) as smtp:
        smtp.login('theashesinetwork@gmail.com', 'huzxxwvfwmfhgpxg')
        smtp.send_message(msg)

    # cur.close()
    # conn.close()
