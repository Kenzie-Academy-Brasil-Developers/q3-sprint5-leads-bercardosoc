import re
from sqlite3 import IntegrityError
from click import MissingParameter
from flask import jsonify, request
from app.exc.leads_exception import InvalidEmail, InvalidPhone
from app.leads_package.leads_services import validate_keys
from app.models.leads_model import LeadModel
from http import HTTPStatus
from app.configs.database import db
from sqlalchemy.exc import IntegrityError

def register_lead():
    expected_keys = {"name", "email", "phone"}
    lead_data = request.get_json()

    for value in list(lead_data.values()):
        if type(value) != str:
            return {"error": "Values must be strings"}, HTTPStatus.BAD_REQUEST
     
    try:
        validate_keys(lead_data, expected_keys)
        lead = LeadModel(**lead_data)

        db.session.add(lead)
        db.session.commit()

    except MissingParameter as e:
        return e.args[0], HTTPStatus.BAD_REQUEST
    
    except KeyError as e:
        return e.args[0], HTTPStatus.BAD_REQUEST

    except InvalidEmail:
        return {"error": "email must contain '@'"}, HTTPStatus.BAD_REQUEST

    except InvalidPhone:
        return {"error": "phone must be in be format '00-00000-0000'"}, HTTPStatus.BAD_REQUEST

    except IntegrityError:
        return {"error": "E-mail or phone already registered"}, HTTPStatus.CONFLICT


    return {
        "name": lead.name,
        "email": lead.email,
        "phone": lead.phone,
        "creation_date": lead.creation_date,
        "last_visit": lead.last_visit,
        "visits": lead.visits
    }, HTTPStatus.CREATED

def list_leads():
    try:
        leads = (
            LeadModel
            .query 
            .all()
        )

        return jsonify(leads), HTTPStatus.OK
    
    except FileNotFoundError:
        return {
            "message": "Nenhum arquivo encontrado"
        }, HTTPStatus.NOT_FOUND

def update_leads_visits():
    ...

def delete_lead():
    ...
