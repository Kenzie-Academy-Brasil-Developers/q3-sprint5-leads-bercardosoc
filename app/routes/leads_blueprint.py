from flask import Blueprint
from app.controllers.leads_controller import register_lead, list_leads, update_leads_visits, delete_lead

bp_leads = Blueprint("bp_leads", __name__, url_prefix="/leads")

bp_leads.get("")(list_leads)
bp_leads.post("")(register_lead)
bp_leads.patch("/<email>")(update_leads_visits)
bp_leads.delete("/<email>")(delete_lead)