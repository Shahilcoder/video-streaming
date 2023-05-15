from flask import Blueprint
from .video import video

api = Blueprint('api', __name__, url_prefix="/api")

api.register_blueprint(video)
