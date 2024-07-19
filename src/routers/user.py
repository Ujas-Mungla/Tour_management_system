import logging
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Header
from typing import List
from database.database import SessionLocal
import uuid
from passlib.context import CryptContext
from src.models.user_mod import User
from src.models.otp_mod import OTP
from src.schemas.user_sch import Users, UserBase, UserCreate, UserUpdate, UsersPatch
from src.utils.token import get_encode_token, decode_token_user_id, decode_token_password, decode_token_user_name, login_token, decode_token_email,decode_token_a_id,decode_token_a_name
from src.schemas.otp_sch import OTPRequest, OTPVerify
import string
import smtplib
import random
from logs.log_config import logger
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from src.utils.otp import generate_otp
from src.routers.admin import Admin


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user = APIRouter()
db = SessionLocal()
Otp = APIRouter()

# ----------------------------------------------encode_token_id------------------------------------------------------

@user.get("/encode_token_id")
def encode_token_id(id: str):
    logger.info(f"Encoding token for ID: {id}")
    access_token = get_encode_token(id)
    return access_token

# ----------------------------------------------Create_User_post------------------------------------------------------

@user.post("/Create_User", response_model=Users)
def create_register_user(user: Users):
    logger.info(f"Creating user: {user.email}")
    find_same_email = db.query(User).filter(User.email == user.email ).first()
    if find_same_email:
        logger.warning(f"Duplicate email found for: {user.email}")
        raise HTTPException(status_code=401, detail="Same E-mail  found please try another one!!!!!!")
    
    find_same_uname = db.query(User).filter( User.username == user.username).first()
    if find_same_uname:
        logger.warning(f"Duplicate  username found for : {user.email}")
        raise HTTPException(status_code=401, detail="Same username found please try another one!!!!!!")

    find_same_mobile_number=db.query(User).filter(User.mobile_no == user.mobile_no).first()
    if find_same_mobile_number:
        logger.warning(f"Duplicate email or username found for: {user.mobile_no}")
        raise HTTPException(status_code=401, detail="Same mobile number found please try another one!!!!!!")
    

    new_user = User(
        id=str(uuid.uuid4()),
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        mobile_no=user.mobile_no,
        password=pwd_context.hash(user.password),
        city=user.city,
    
    )
    db.add(new_user)
    db.commit()
    logger.success(f"User created successfully: {user.email}")
    return new_user

# ----------------------------------------------get_all_users------------------------------------------------------

@user.get("/get_user_all_details",response_model=list[UserBase])
def get_user_all_details(token= Header(...)):
    admin_name=decode_token_a_name(token)
    # breakpoint()
    db_admin=db.query(Admin).filter(Admin.user_name == admin_name,Admin.is_active == True,Admin.is_deleted == False).first()
  
            
    if db_admin is  None:
        raise HTTPException(status_code=200,detail="invalid token")
    
    logger.info(f"Fetching all details ")
    db_user=db.query(User).filter(User.is_active == True,User.is_deleted == False,User.is_deleted == False,User.is_verified == True).all()

    if db_user is None:
        logger.warning(f"No active user")
        raise HTTPException(status_code=404,detail="user not found")
    
    logger.success(f"User details fetched successfully")
    return db_user

# ----------------------------------------------get_user_by_token_id------------------------------------------------------

@user.get("/get_user_by_token_id/", response_model=Users)
def get_employee_by_id(token=Header(...)):
    logger.info(f"Fetching user by token")
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id, User.is_active == True, User.is_verified == True).first()
    if db_user is None:
        logger.warning(f"User not found for token: {token}")
        raise HTTPException(status_code=404, detail="User Not Found !!!")
    return db_user

# # ----------------------------------------------update_user_by_token------------------------------------------------------

@user.put("/update_user_by_token/")
def update_user_data(user: Users, token=Header(...)):
    logger.info(f"Updating user by token")
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id, User.is_active == True, User.is_verified == True).first()
    if db_user is None:
        logger.warning(f"User not found for token: {token}")
        raise HTTPException(status_code=404, detail="User Not Found!!!!")
    
    existiong_user = db.query(User).filter(User.username == user.username).first()
    if existiong_user:
        logger.warning(f"Username already exists: {user.username}")
        raise HTTPException(status_code=404, detail="User already exist!!!!")
    
    existiong_email = db.query(User).filter(User.email == user.email).first()
    if existiong_email:
        logger.warning(f"E-mail already exists: {user.email}")
        raise HTTPException(status_code=404, detail="E-mail already exist!!!!")
    
    existiong_phoneno = db.query(User).filter(User.mobile_no == user.mobile_no).first()
    if existiong_phoneno:
        logger.warning(f"E-mail already exists: {user.mobile_no}")
        raise HTTPException(status_code=404, detail="Mobile-NO already exist!!!!")
    


    db_user.first_name = user.first_name,
    db_user.last_name = user.last_name,
    db_user.username = user.username,
    db_user.email = user.email,
    db_user.mobile_no = user.mobile_no,
    db_user.password = pwd_context.hash(user.password),
    db_user.city = user.city
    
    db.commit()
    logger.success(f"User details updated successfully for token: {token}")
    return "Your Detail Changed Successfully!!!!!!!!!!!"

# ----------------------------------------------update[PATCH]_user_by_token------------------------------------------------------

@user.patch("/update_user_patch")
def update_employee_patch(employeee: UsersPatch, token=Header(...)):
    logger.info(f"Patching user details by token")
    user_id = decode_token_user_id(token)
    find_user = db.query(User).filter(User.id == user_id, User.is_active == True, User.is_verified == True).first()
    if find_user is None:
        logger.warning(f"User not found for token: {token}")
        raise HTTPException(status_code=404, detail="User Not Found")
    update_data = employeee.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(find_user, key, value)
    db.commit()
    db.refresh(find_user)
    logger.success(f"User details patched successfully for token: {token}")
    return {"message": "Details changed successfully", "User": find_user}

# ----------------------------------------------Delete_User_by_token------------------------------------------------------

@user.delete("/delete_user_by_token/")
def delete_employee(token=Header(...)):
    emp_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == emp_id, User.is_active == True, User.is_verified == True).first()
    if db_user is None:
        logger.warning(f"User not found for token: {token}")
        raise HTTPException(status_code=404, detail="User Not Found.....")
    db_user.is_active = False
    db_user.is_deleted = True
    db.delete(db_user)
    db.commit()
    logger.success(f"User deleted successfully for token: {token}")
    return "User Deleted Successfully !!!!!!!!!!!!!"

# --------------------------------------------------GENERATE_OTP ------------------------------------------------------------

def generate_otp(email: str):
    logger.info(f"Generating OTP for email: {email}")
    otp_code = str(random.randint(100000, 999999))
    expiration_time = datetime.now() + timedelta(minutes=5)
    
    otp_entry = OTP(
        email=email,
        otp=otp_code,
        expired_time=expiration_time,
    )
    db.add(otp_entry)
    db.commit()
    logger.success(f"OTP generated: {otp_code} for email: {email}")
    return otp_code

def send_otp_email(email: str, otp_code: str):
    logger.info(f"Sending OTP email to: {email}")
    sender_email = "ujasmungla@gmail.com"
    password = "wfrdhevqfopcssre"
    subject = "Your OTP Code"
    message_text = f"Your OTP is {otp_code} which is valid for 5 minutes"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(message_text, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message.as_string())
        server.quit()
        logger.info(f"OTP email sent successfully to: {email}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

@Otp.post("/generate_otp/")
def generate_otp_endpoint(request: OTPRequest):
    email = request.email  
    logger.info(f"OTP request received for email: {email}")
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        logger.warning(f"User not found for email: {email}")
        raise HTTPException(status_code=404, detail="User not found")
    otp_code = generate_otp(email)
    send_otp_email(email, otp_code)
    return {"message": "OTP generated and sent successfully to the provided email address."}

# --------------------------------------------------VERIFICATION_OTP ------------------------------------------------------------

@Otp.post("/verify_otp")
def verify_otp(otp_verify: OTPVerify):
    logger.info(f"Verifying OTP for email: {otp_verify.email}")
    otp_entry = db.query(OTP).filter(
        OTP.email == otp_verify.email,
        OTP.otp == otp_verify.otp,
        OTP.is_active == True,
        OTP.expired_time > datetime.now(),
    ).first()

    if not otp_verify.email:
        logger.warning("Email ID not provided for OTP verification")
        raise HTTPException(status_code=400, detail="Please enter email ID")
    if otp_entry is None:
        logger.warning(f"Invalid or expired OTP for email: {otp_verify.email}")
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    otp_entry.is_active = False  
    user = db.query(User).filter(User.email == otp_verify.email).first()
    if user is None:
        logger.warning(f"User not found for email: {otp_verify.email}")
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    db.delete(otp_entry)
    db.commit()
    logger.success(f"OTP verified successfully for email: {otp_verify.email}")
    return {"message": "OTP verified successfully"}

# ---------------------------------------------encode_token_login-----------------------------------------------------

@user.get("/encode_token_login")
def encode_token_id(id: str, password: str, email: str):
    logger.info(f"Encoding login token for ID: {id}, email: {email}")
    access_token = login_token(id, password, email)
    return access_token

# ----------------------------------------------LOGIN_USER-----------------------------------------------------

@user.get("/logging_users")
def logging_user(email: str, password: str):
    logger.info(f"Logging in user: {email}")
    db_user = db.query(User).filter(User.email == email, User.is_active == True, User.is_deleted == False, User.is_verified == True).first()
    if db_user is None:
        logger.warning(f"User not found: {email}")
        raise HTTPException(status_code=404, detail="User not found")
    if not pwd_context.verify(password, db_user.password):
        logger.warning(f"Incorrect password for user: {email}")
        raise HTTPException(status_code=404, detail="Password is incorrect")
    access_token = login_token(db_user.id, email, db_user.username)
    logger.success(f"User logged in successfully: {email}")
    return access_token

# ----------------------------------------------forgotpass_user_by_token------------------------------------------------------

@user.put("/forgotpass_user_by_token/")
def forgotpass_user_by_token(new_pass: str, token=Header(...)):
    logger.info("Handling forgot password request")
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id, User.is_active == True, User.is_verified == True).first()
    if db_user is None:
        logger.warning(f"User not found for token: {token}")
        raise HTTPException(status_code=404, detail="User Not Found!!!")
    db_user.password = pwd_context.hash(new_pass)
    db.commit()
    logger.success(f"Password changed successfully for user ID: {user_id}")
    return "Password Change Successfully"

# ----------------------------------------------reset_pass_user_token------------------------------------------------------

@user.put("/reset_pass_user_token/")
def reset_pass_user(old_pass: str, new_pass: str, token=Header(...)):
    logger.info("Handling reset password request")
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id, User.is_active == True, User.is_verified == True).first()
    if not db_user:
        logger.warning(f"User not found for token: {token}")
        raise HTTPException(status_code=404, detail="User not found")
    if pwd_context.verify(old_pass, db_user.password):
        db_user.password = pwd_context.hash(new_pass)
        db.commit()
        logger.success(f"Password reset successfully for user ID: {user_id}")
        return {"message": "Password Reset Successfully!!!"}
    else:
        logger.warning(f"Old password does not match for user ID: {user_id}")
        raise HTTPException(status_code=400, detail="Old password does not match")







