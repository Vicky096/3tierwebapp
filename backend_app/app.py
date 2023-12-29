
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:user123@localhost:5432/cust_db'  # SQLite database file
db = SQLAlchemy(app)
CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password
        })
    return jsonify({'users': user_list})

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
    	return jsonify({'error': 'Missing parameters'}), 400

    existing_user = User.query.filter_by(username=username).first()   
    if existing_user:
    	return jsonify({'error': 'Username already exists'}), 400

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

if __name__ == '__main__':
 #   db.create_all()
    app.run(debug=True)

