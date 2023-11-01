import uuid
from sqlalchemy.orm import Session
from scurity import get_password_hash
from connection import Base, engine, sess_db
from models import PaymentFormCreate, PaymentForm
from fastapi import FastAPI, Depends, Form, HTTPException, Request

# Repository
from repository_user import UserRepository, SendEmailVerify

# Model
from models import UserModel


app = FastAPI()
# db engin
Base.metadata.create_all(bind=engine)


@app.post("/sign-up-user")
def signup_user(db: Session = Depends(sess_db), username: str = Form(), email: str = Form(), password: str = Form()):
    user_repository = UserRepository(db)
    db_user = user_repository.get_user_by_username(email)
    if db_user:
        data = {
            "status": 409,
            "msg": "User Already Exists"
        }
        return data
    else:
        user = UserModel(email=email, username=username, password=get_password_hash(password))
        success = user_repository.create_user(user)

        # Sending Mail

        user_name = user.username
        email = user.email
        SendEmailVerify.send_verify(user_name, email)
        if success:
            data = {
                "user_name": username,
                "email": email,
                "status": 201,
                "msg": "Create User Successfully"
            }
            return data
        else:
            raise HTTPException(
                status_code=401, detail="Credentials not correct"
            )


@app.post("/users/{user_id}/payment_forms/")
def create_payment_form(request: Request, user_id: int, payment_form: PaymentFormCreate,
                        db: Session = Depends(sess_db)):
    new_uuid = uuid.uuid4()
    db_payment_form = PaymentForm(**payment_form.dict(), owner_id=user_id, unique_link=str(new_uuid))
    records = db.query(PaymentForm).all()
    print(records)

    if db_payment_form:
        record = db.query(PaymentForm).filter(PaymentForm.owner_id == user_id).first()
        client_ip = f"{request.client.host}:8000"
        payment_link = f"https://{client_ip}/payment-form/{str(new_uuid)}"
        db.add(db_payment_form)
        db.commit()
        db.refresh(db_payment_form)

        # Access the 'status' attribute of the record
        user_details = db.query(UserModel).filter(UserModel.id == user_id).first()

        #  Sending Mail
        email = user_details.email
        user_name = user_details.username
        status = record.status
        SendEmailVerify.send_payment_verify(user_name, email)
        data = {
            "id": user_id,
            "unique_link": payment_link,
            "unique_payment_form_id": new_uuid,
            "status": status,
            "msg": "Payment Processing"
        }
        return data
    else:
        return "Payment Failed"


@app.post("/payment-form/{unique_payment_form_id}")
def get_payment_form(unique_payment_form_id: str, db: Session = Depends(sess_db)):
    payment_form_data = db.query(PaymentForm).filter(PaymentForm.unique_link == unique_payment_form_id).first()
    if payment_form_data:
        if payment_form_data.status == "Pending":
            payment_form_data.status = "Success"
            db.add(payment_form_data)
            db.commit()
            data = {
                    "id": unique_payment_form_id,
                    "status": payment_form_data.status,
                    "msg": "Payment Successful"
                }
            return data
        else:
            raise HTTPException(status_code=201, detail="Payment Already Initiated")
    else:
        raise HTTPException(status_code=404, detail="Payment form not found")


@app.get("/get_payment_details/{unique_payment_form_id}")
async def get_payment_details(unique_payment_form_id: str, db: Session = Depends(sess_db)):
    payment_form_data = db.query(PaymentForm).filter(PaymentForm.unique_link == unique_payment_form_id).first()

    if payment_form_data:
        data = {
            "name": payment_form_data.name,
            "description": payment_form_data.description,
            "amount": payment_form_data.amount,
            "currency": payment_form_data.currency,
            "status": payment_form_data.status,
        }
        return data
    else:
        raise HTTPException(status_code=404, detail="Payment not found")
