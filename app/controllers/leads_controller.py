from http import HTTPStatus
from datetime import datetime
from click import MissingParameter
from flask import jsonify, request
from sqlite3 import IntegrityError
from app.configs.database import db
from app.models.leads_model import LeadModel
from sqlalchemy.exc import IntegrityError, NoResultFound, ProgrammingError
from app.leads_package.leads_services import validate_keys
from app.exc.leads_exception import InvalidEmail, InvalidPhone

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

        return jsonify(lead), HTTPStatus.CREATED

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

def list_leads():
    try:
        """ leads = (
            LeadModel
            .query 
            .all()
        ) """

        leads = LeadModel.query.order_by(
            LeadModel.visits.desc()
        ).all()

        return jsonify(leads), HTTPStatus.OK
    
    except FileNotFoundError:
        return {
            "message": "File or table not found"
        }, HTTPStatus.NOT_FOUND

def update_leads_visits():
    expected_keys = {"email"}
    lead_data = request.get_json()

    try:
        validate_keys(lead_data, expected_keys)
        email = lead_data["email"]
        lead_data = LeadModel.query.filter_by(email=email).one()

        setattr(lead_data, "last_visit", datetime.now())
        setattr(lead_data, "visits", (lead_data.__dict__["visits"] + 1))

        db.session.add(lead_data)
        db.session.commit()

        return "", HTTPStatus.ACCEPTED

    except KeyError as e:
        return e.args[0], HTTPStatus.BAD_REQUEST

    except ProgrammingError:
        return {"error": "email must be a string"}, HTTPStatus.BAD_REQUEST

    except NoResultFound:
        return {"error": "E-mail not found. E-mail must contain '@'."}, HTTPStatus.BAD_REQUEST
        

def delete_lead():
    expected_keys = {"email"}
    lead_data = request.get_json()
    
    try: 
        validate_keys(lead_data, expected_keys)
        email = lead_data["email"]
        lead_data = LeadModel.query.filter_by(email=email).one()

        db.session.delete(lead_data)
        db.session.commit()

        return "", HTTPStatus.NO_CONTENT

    except KeyError as e:
        return e.args[0], HTTPStatus.BAD_REQUEST

    except ProgrammingError:
        return {"error": "email must be a string"}, HTTPStatus.BAD_REQUEST

    except NoResultFound:
        return {
            "error": "E-mail not found. E-mail should be a valid string."
        }, HTTPStatus.NOT_FOUND
