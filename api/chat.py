from flask import Blueprint, render_template, request, redirect, url_for

chat_bp = Blueprint('chat', __name__)