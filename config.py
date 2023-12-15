from os import getenv
from dotenv import load_dotenv

load_dotenv()

# database connection
SECRET_KEY = getenv("SECRET_KEY")
DB_NAME = getenv("DB_NAME")
DB_USERNAME = getenv("DB_USERNAME")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")

# mailtrap connection
MAIL_SERVER = getenv("MAIL_SERVER")
MAIL_PORT = getenv("MAIL_PORT")
MAIL_USERNAME = getenv("MAIL_USERNAME")
MAIL_PASSWORD = getenv("MAIL_PASSWORD")
MAIL_USE_TLS = True
MAIL_USE_SSL = False

# cloudinary connection
cloud_name = getenv("cloud_name")
api_key = getenv("api_key")
api_secret = getenv("api_secret")