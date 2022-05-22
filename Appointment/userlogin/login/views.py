from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import db


views = Blueprint('views', __name__)



