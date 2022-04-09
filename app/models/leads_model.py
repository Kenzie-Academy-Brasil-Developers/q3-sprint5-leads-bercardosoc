from app.exc.leads_exception import InvalidEmail, InvalidPhone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import validates
from app.configs.database import db
from dataclasses import dataclass
from datetime import datetime
import re

@dataclass
class LeadModel(db.Model):

    name: str 
    email: str
    phone: str 
    creation_date: datetime
    last_visit: datetime 
    visits: int 

    __tablename__ = "the_leads"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    creation_date = Column(DateTime, default=datetime.now()) 
    last_visit = Column(DateTime, default=datetime.now()) 
    visits = Column(Integer, default=1) 

    @validates("email")
    def validate_email(self, _, email_to_be_tested):
        if "@" not in email_to_be_tested:
            raise InvalidEmail
        return email_to_be_tested

    @validates("phone")
    def validate_phone(self, _, phone_to_be_tested):

        ddd = r"^(\([1-9]{2}\))"
        phone_number = r"(\s?\d{5}-?\d{4})$"
        phone_exp = ddd + phone_number
        phone_regex = re.compile(phone_exp)

        if not re.fullmatch(phone_regex, phone_to_be_tested):
            raise InvalidPhone 

        return phone_to_be_tested
