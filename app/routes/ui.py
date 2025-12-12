# app/routes/ui.py

from flask import Blueprint, render_template, request, redirect, url_for, current_app

ui_bp = Blueprint('ui', __name__)

# Homepage redirect
@ui_bp.route('/')
def home():
    

@ui_bp.route('/passwords', methods=["GET", "POST"])
def password_list():
    