from dataclasses import dataclass
from datetime import datetime
from email.policy import default
from enum import unique
from app.configs.database import db
from sqlalchemy import Column, Integer, String, DateTime

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
    creation_date = Column(DateTime) 
    last_visit = Column(DateTime) 
    visits = Column(Integer, default=1) 