import smtplib
from models import UserModel
from sqlalchemy.orm import Session
from email.message import EmailMessage


class UserRepository:
    def __init__(self, sess: Session):
        self.sess: Session = sess

    def create_user(self, signup: UserModel) -> bool:
        try:
            self.sess.add(signup)
            self.sess.commit()
        except:
            return False
        return True

    def get_user_by_username(self, email: str):
        return self.sess.query(UserModel).filter(UserModel.email == email).first()


class SendEmailVerify:

    @classmethod
    def send_verify(cls, user_name, email):
        email_address = "jaforakib@gmail.com"  # type Email
        email_password = "pmbi pfpo giog ecpr"  # If you do not have a gmail apps password, create a new app with
        # using generate password. Check your apps and passwords
        # https://myaccount.google.com/apppasswords

        # create email
        msg = EmailMessage()
        msg['Subject'] = "Account Open Successfully"
        msg['From'] = email_address
        msg['To'] = email  # type Email
        msg.set_content(
            f"""\
    Dear {user_name},    
    Your Payment Account Create Successfully.
    """,

        )
        # send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)

    @classmethod
    def send_payment_verify(cls, user_name, email):
        email_address = "jaforakib@gmail.com"  # type Email
        email_password = "pmbi pfpo giog ecpr"  # If you do not have a gmail apps password, create a new app with
        # using generate password. Check your apps and passwords
        # https://myaccount.google.com/apppasswords

        # create email
        msg = EmailMessage()
        msg['Subject'] = "Successfully Payment"
        msg['From'] = email_address
        msg['To'] = email  # type Email
        msg.set_content(
            f"""\
    Dear {user_name},    
    Your Payment Successfully Initiated.
    """,

        )
        # send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
