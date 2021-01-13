class Config:
    SECRET_KEY = "0d2e81519f6420437ca98c44c704bf6a"
    SQLALCHEMY_TRACK_MODIFICATIONS = "False"
    # SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    # SQLALCHEMY_DATABASE_URI = (
    #     "mysql://admin:Gundusaarav@1234@127.0.0.1:{}/flask".format(tunnel)
    # )
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
