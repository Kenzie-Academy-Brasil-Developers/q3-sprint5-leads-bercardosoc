from flask import Flask
from flask_migrate import Migrate

def init_app(app: Flask):
    from app.models.leads_model import LeadModel 

    Migrate(app, app.db)