from flask import Blueprint
from api.models.user import User

# set route
user = Blueprint('user_router', __name__)


@job.route('/<int:id>', methods=['GET'])
def getUser(id):
    user = User.searchBy(id)
    print(user)
