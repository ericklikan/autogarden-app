import os
from flask import request, Blueprint, send_from_directory, render_template


view = Blueprint('view',__name__)

@view.route('/')
def index():
    return render_template('index.html')