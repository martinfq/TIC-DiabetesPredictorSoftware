from flask import jsonify, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

login_manager = LoginManager()
login_manager.init_app(app)

jwt = JWTManager(app)

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

users = {'user1': User(id=1, username='user1')}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user
    return None

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    if username in users:
        user = users[username]
        login_user(user)
        access_token = create_access_token(identity={'id': user.id, 'username': user.username})
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    identity = get_jwt_identity()
    return jsonify(logged_in_as=identity), 200

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"msg": "Logged out"}), 200

if __name__ == '__main__':
    app.run()
