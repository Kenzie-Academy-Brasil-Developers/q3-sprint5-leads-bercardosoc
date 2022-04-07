import re
from flask import jsonify, request
from app.exc.leads_exception import InvalidEmail, InvalidPhone
from app.models.leads_model import LeadModel
from http import HTTPStatus
from app.configs.database import db

def register_lead():
    lead_data = request.get_json()
    
    try:
        lead = LeadModel(**lead_data)

    except InvalidEmail:
        return {"error": "email must contain '@'"}, HTTPStatus.BAD_REQUEST
    except InvalidPhone:
        return {"error": "phone must be in be format '00-00000-0000' or '000-00000-0000'"}, HTTPStatus.BAD_REQUEST

    db.session.add(lead)
    db.session.commit()

    return {
        "name": lead.name,
        "email": lead.email,
        "phone": lead.phone,
        "creation_date": lead.creation_date,
        "last_visit": lead.last_visit,
        "visits": lead.visits
    }, HTTPStatus.CREATED

def list_leads():
    ...

def update_leads_visits():
    ...

def delete_lead():
    ...
