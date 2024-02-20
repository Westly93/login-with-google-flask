from urllib.parse import quote_plus

password = 'Dzidzo@MSU2022'
encoded_password = quote_plus(password)
DB_NAME = "database.db"
# DB_NAME = "learn"


class Config:
    GOOGLE_CLIENT_ID = "1091373261442-1oro7ar3b9l01pi7n682lqr3en9417um.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "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"
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
    SECRET_KEY = 'westly2001'
    SERVER_NAME = "127.0.0.1:5001"
    SSL_CERTIFICATE = "cert.pem"
    SSL_KEY = "key.pem"
    # SQLALCHEMY_DATABASE_URI = f'mysql://username:password@localhost/{DB_NAME}'
    # SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:{encoded_password}@localhost/{DB_NAME}'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
    # Email settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = 'flaskapp/static/uploads'
    COURSES_PER_PAGE = 1
    RESET_PASS_TOKEN_MAX_AGE = 3600
    SECURITY_PASSWORD_SALT = "Dzidzo@MSU2022"
    MAIL_DEFAULT_SENDER = "admin@courses.msu.ac.zw"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEBUG = False
    MAIL_USERNAME = 'admin@courses.msu.ac.zw'
    MAIL_PASSWORD = "demc jbsb dgqi hrwf"
    # EMAIL_USE_TLS = True
