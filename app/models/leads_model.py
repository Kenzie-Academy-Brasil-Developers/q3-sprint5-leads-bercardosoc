from app.exc.leads_exception import InvalidEmail, InvalidFields, InvalidPhone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import validates
from app.configs.database import db
from dataclasses import dataclass
from datetime import datetime
import re

@dataclass
class LeadModel(db.Model):

    id: int 
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
        if not re.match(r"(?:\+?\(?\d{2}?\)?\D?)?\d{5}\D?\d{4}", phone_to_be_tested):
            raise InvalidPhone 
        return phone_to_be_tested

    """ @validates("email", "phone", "name")
    def validate_entered_fields(self, _, email_to_be_tested, phone_to_be_tested, name_to_be_tested):
        if type(email_to_be_tested) or type(phone_to_be_tested) or type(name_to_be_tested) != str:
            raise InvalidFields
        return email_to_be_tested, phone_to_be_tested, name_to_be_tested
 """