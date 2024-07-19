from fastapi import FastAPI, HTTPException, APIRouter, Depends, Header
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import logging
from database.database import SessionLocal
from src.schemas.addr_sch import AddressBase, AddrPatch
from src.models.address_mod import Address
from src.routers.admin import Admin
from src.utils.token import decode_token_a_name
import uuid
from logs.log_config import logger  # Import the logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
addr = APIRouter()
db = SessionLocal()

@addr.post("/create_address_information", response_model=AddressBase)
def create_address(address: AddressBase):
    logger.info(f"Creating address for user_id: {address.user_id}, tour_id: {address.tour_id}")
    new_address = Address(
        address_id=str(uuid.uuid4()),
        user_id=address.user_id,
        tour_id=address.tour_id,
        address=address.address,
        city=address.city,
        state=address.state,
        pincode=address.pincode,
        country=address.country
    )
    db.add(new_address)
    db.commit()
    logger.success(f"Address created successfully with address_id: {new_address.address_id}")
    return new_address

@addr.get("/get_all_address/", response_model=List[AddressBase])
def get_all_address(token: str = Header(...)):
    logger.info("Fetching all addresses")
    admin_name = decode_token_a_name(token)
    db_admin = db.query(Admin).filter(Admin.user_name == admin_name, Admin.is_active == True, Admin.is_deleted == False).first()
    if db_admin is None:
        logger.warning("Invalid token provided")
        raise HTTPException(status_code=200, detail="Invalid token")
    db_address = db.query(Address).filter(Address.is_active == True).all()
    if not db_address:
        logger.warning("No addresses found")
        raise HTTPException(status_code=404, detail="Address not found")
    logger.success(f"Fetched {len(db_address)} addresses")
    return db_address

@addr.get("/get_address_by_id/{address_id}", response_model=AddressBase)
def get_address_by_id(address_id: str):
    logger.info(f"Fetching address by id: {address_id}")
    db_address = db.query(Address).filter(Address.address_id == address_id).first()
    if db_address is None:
        logger.warning(f"Address not found with id: {address_id}")
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@addr.patch("/update_address/{address_id}", response_model=AddrPatch)
def update_address(address_id: str, ad: AddrPatch):
    logger.info(f"Updating address with id: {address_id}")
    db_addr = db.query(Address).filter(Address.address_id == address_id).first()
    if db_addr is None:
        logger.warning(f"Address not found with id: {address_id}")
        raise HTTPException(status_code=404, detail="Address not found")
    for key, value in ad.dict(exclude_unset=True).items():
        setattr(db_addr, key, value)
    db.commit()
    db.refresh(db_addr)
    logger.success(f"Address with id: {address_id} updated successfully")
    return db_addr

@addr.delete("/delete_address_information/{addr_info_id}")
def delete_address(addr_info_id: str):
    logger.info(f"Deleting address with id: {addr_info_id}")
    db_addr_info = db.query(Address).filter(Address.address_id == addr_info_id).first()
    if not db_addr_info:
        logger.warning(f"Address not found with id: {addr_info_id}")
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_addr_info)
    db.commit()
    logger.success(f"Address with id: {addr_info_id} deleted successfully")
    return f"Your address deleted successfully!!!"
