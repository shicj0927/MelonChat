from flask import Blueprint, render_template, request, redirect, url_for

note_bp = Blueprint('note', __name__)