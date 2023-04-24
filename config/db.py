from flask_sqlalchemy import SQLAlchemy
import psycopg2

db = SQLAlchemy()
conn = psycopg2.connect(
    host="dpg-ch38n03h4hsum425q240-a.frankfurt-postgres.render.com",
    database="ashesi_net",
    user="jonathan",
    password="nnAXv21VCyJoZakGmt6xTXICWg9F4aTT"
)