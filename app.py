from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/personalcolor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)

    def __init__(self, nama, email, password):
        self.nama = nama
        self.email = email
        self.password = generate_password_hash(password, method='scrypt')

    def check_password(self, password):
        return check_password_hash(self.password, password)

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/produk')
def produk():
    return render_template('produk.html')

@app.route('/deteksi')
def deteksi():
    return render_template('deteksi.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        nama = data.get('nama')
        email = data.get('email')
        password = data.get('password')
        
        print(f"Register attempt - Email: {email}, Password: {password}")
        
        if not nama or not email or not password:
            return jsonify({"error": "Nama, email, and password are required."}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email is already registered."}), 400
        
        if User.query.filter_by(nama=nama).first():
            return jsonify({"error": "Nama is already taken."}), 400

        new_user = User(nama=nama, email=email, password=password)
        print(f"Hashed password during registration: {new_user.password}")
        
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "Registration successful!",
            "email": email,
            "nama": nama
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        print(f"Login attempt - Email: {email}, Password: {password}")
        
        if not email or not password:
            return jsonify({"error": "Email and password are required."}), 400

        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({"error": "User not found."}), 404
        
        print(f"Stored hashed password: {user.password}")
        print(f"Password check result: {user.check_password(password)}")
        
        if user.check_password(password):
            return jsonify({
                "message": "Login successful!",
                "email": user.email,
                "nama": user.nama
            }), 200
        else:
            return jsonify({"error": "Invalid email or password."}), 401
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({"error": f"Login failed: {str(e)}"}), 500

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = [{"id": user.id, "nama": user.nama, "email": user.email} for user in users]
    return jsonify(users_data), 200

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)