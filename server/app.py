from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from werkzeug.security import generate_password_hash
from models import db, User, Employment, Category, Application, SocialIntegration, Funding, FundingApplication
from applications import applications_bp

def create_app():
    app = Flask(__name__)

    # Configure your database URI here
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poverty.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'go high'  # Set your secret key
    app.register_blueprint(applications_bp)

    # Initialize the database and Flask-Migrate
    db.init_app(app)
    migrate = Migrate(app, db)
    
    api = Api(app)
    # Initialize other routes or blueprints as needed

    return app

app = create_app()

# User routes
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not all(key in data for key in ['username', 'email', 'password']):
        return jsonify({'message': 'Missing required fields!'}), 400

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        profile_picture=data.get('profile_picture')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!', 'user_id': new_user.id}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'profile_picture': user.profile_picture
        } for user in users
    ]), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'profile_picture': user.profile_picture
        }), 200
    return jsonify({'message': 'User not found!'}), 404 

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found!'}), 404

    data = request.get_json()
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = generate_password_hash(data['password'])
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'profile_picture' in data:
        user.profile_picture = data['profile_picture']

    db.session.commit()
    return jsonify({'message': 'User updated successfully!'}), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully!'}), 200
    return jsonify({'message': 'User not found!'}), 404

# Category routes
@app.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get(id)
    if category:
        return jsonify({
            'id': category.id,
            'name': category.name,
            'description': category.description,
        }), 200
    return jsonify({'message': 'Category not found'}), 404

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([
        {
            'id': category.id,
            'name': category.name,
            'description': category.description,
        } for category in categories
    ]), 200

@app.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    if not data or not all(key in data for key in ['name']):
        return jsonify({'message': 'Missing required fields!'}), 400

    new_category = Category(
        name=data['name'],
        description=data.get('description'),
        user_id=data.get('user_id')
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category created successfully!', 'category_id': new_category.id}), 201

@app.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({'message': 'Category not found!'}), 404

    data = request.get_json()
    if 'name' in data:
        category.name = data['name']
    if 'description' in data:
        category.description = data['description']

    db.session.commit()
    return jsonify({'message': 'Category updated successfully!'}), 200

@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully!'}), 200
    return jsonify({'message': 'Category not found!'}), 404

# Employment routes
@app.route('/employments', methods=['POST'])
def create_employment():
    data = request.get_json()
    if not data or not all(key in data for key in ['user_id', 'category_id', 'title', 'description']):
        return jsonify({'message': 'Missing required fields!'}), 400

    employment = Employment(
        user_id=data['user_id'],
        category_id=data['category_id'],
        title=data['title'],
        description=data['description'],
        requirements=data.get('requirements'),
        location=data.get('location'),
        salary_range=data.get('salary_range')
    )
    db.session.add(employment)
    db.session.commit()
    return jsonify({'message': 'Employment created successfully!', 'employment_id': employment.id}), 201

@app.route('/employments', methods=['GET'])
def get_employments():
    employments = Employment.query.all()
    return jsonify([
        {
            'id': employment.id,
            'user_id': employment.user_id,
            'category_id': employment.category_id,
            'title': employment.title,
            'description': employment.description,
            'requirements': employment.requirements,
            'location': employment.location,
            'salary_range': employment.salary_range
        } for employment in employments
    ]), 200

@app.route('/employments/<int:id>', methods=['GET'])
def get_employment(id):
    employment = Employment.query.get(id)
    if employment:
        return jsonify({
            'id': employment.id,
            'user_id': employment.user_id,
            'category_id': employment.category_id,
            'title': employment.title,
            'description': employment.description,
            'requirements': employment.requirements,
            'location': employment.location,
            'salary_range': employment.salary_range
        }), 200
    return jsonify({'message': 'Employment not found!'}), 404

@app.route('/employments/<int:id>', methods=['PUT'])
def update_employment(id):
    employment = Employment.query.get(id)
    if not employment:
        return jsonify({'message': 'Employment not found!'}), 404

    data = request.get_json()
    if 'title' in data:
        employment.title = data['title']
    if 'description' in data:
        employment.description = data['description']
    if 'requirements' in data:
        employment.requirements = data['requirements']
    if 'location' in data:
        employment.location = data['location']
    if 'salary_range' in data:
        employment.salary_range = data['salary_range']

    db.session.commit()
    return jsonify({'message': 'Employment updated successfully!'}), 200

@app.route('/employments/<int:id>', methods=['DELETE'])
def delete_employment(id):
    employment = Employment.query.get(id)
    if employment:
        db.session.delete(employment)
        db.session.commit()
        return jsonify({'message': 'Employment deleted successfully!'}), 200
    return jsonify({'message': 'Employment not found!'}), 404

# Social Integration routes
@app.route('/social_integrations', methods=['POST'])
def create_social_integration():
    data = request.get_json()
    if not data or not all(key in data for key in ['user_id', 'category_id', 'association_name', 'description']):
        return jsonify({'message': 'Missing required fields!'}), 400

    new_social_integration = SocialIntegration(
        user_id=data['user_id'],
        category_id=data['category_id'],
        association_name=data['association_name'],
        description=data['description']
    )
    db.session.add(new_social_integration)
    db.session.commit()
    return jsonify({'message': 'Social Integration created successfully!', 'id': new_social_integration.id}), 201

@app.route('/social_integrations', methods=['GET'])
def get_social_integrations():
    social_integrations = SocialIntegration.query.all()
    return jsonify([
        {
            'id': si.id,
            'user_id': si.user_id,
            'category_id': si.category_id,
            'association_name': si.association_name,
            'description': si.description
        } for si in social_integrations
    ]), 200

@app.route('/social_integrations/<int:id>', methods=['GET'])
def get_social_integration(id):
    social_integration = SocialIntegration.query.get(id)
    if social_integration:
        return jsonify({
            'id': social_integration.id,
            'user_id': social_integration.user_id,
            'category_id': social_integration.category_id,
            'association_name': social_integration.association_name,
            'description': social_integration.description
        }), 200
    return jsonify({'message': 'Social Integration not found!'}), 404

@app.route('/social_integrations/<int:id>', methods=['PUT'])
def update_social_integration(id):
    social_integration = SocialIntegration.query.get(id)
    if not social_integration:
        return jsonify({'message': 'Social Integration not found!'}), 404

    data = request.get_json()
    if 'association_name' in data:
        social_integration.association_name = data['association_name']
    if 'description' in data:
        social_integration.description = data['description']

    db.session.commit()
    return jsonify({'message': 'Social Integration updated successfully!'}), 200

@app.route('/social_integrations/<int:id>', methods=['DELETE'])
def delete_social_integration(id):
    social_integration = SocialIntegration.query.get(id)
    if social_integration:
        db.session.delete(social_integration)
        db.session.commit()
        return jsonify({'message': 'Social Integration deleted successfully!'}), 200
    return jsonify({'message': 'Social Integration not found!'}), 404

# Funding routes
@app.route('/fundings', methods=['POST'])
def create_funding():
    data = request.get_json()
    if not data or not all(key in data for key in ['user_id', 'amount', 'description']):
        return jsonify({'message': 'Missing required fields!'}), 400

    new_funding = Funding(
        user_id=data['user_id'],
        amount=data['amount'],
        description=data['description']
    )
    db.session.add(new_funding)
    db.session.commit()
    return jsonify({'message': 'Funding created successfully!', 'id': new_funding.id}), 201

@app.route('/fundings', methods=['GET'])
def get_fundings():
    fundings = Funding.query.all()
    return jsonify([
        {
            'id': funding.id,
            'user_id': funding.user_id,
            'amount': funding.amount,
            'description': funding.description
        } for funding in fundings
    ]), 200

@app.route('/fundings/<int:id>', methods=['GET'])
def get_funding(id):
    funding = Funding.query.get(id)
    if funding:
        return jsonify({
            'id': funding.id,
            'user_id': funding.user_id,
            'amount': funding.amount,
            'description': funding.description
        }), 200
    return jsonify({'message': 'Funding not found!'}), 404

@app.route('/fundings/<int:id>', methods=['PUT'])
def update_funding(id):
    funding = Funding.query.get(id)
    if not funding:
        return jsonify({'message': 'Funding not found!'}), 404

    data = request.get_json()
    if 'amount' in data:
        funding.amount = data['amount']
    if 'description' in data:
        funding.description = data['description']

    db.session.commit()
    return jsonify({'message': 'Funding updated successfully!'}), 200

@app.route('/fundings/<int:id>', methods=['DELETE'])
def delete_funding(id):
    funding = Funding.query.get(id)
    if funding:
        db.session.delete(funding)
        db.session.commit()
        return jsonify({'message': 'Funding deleted successfully!'}), 200
    return jsonify({'message': 'Funding not found!'}), 404

# Funding Application routes
@app.route('/funding_applications', methods=['POST'])
def create_funding_application():
    data = request.get_json()
    if not data or not all(key in data for key in ['user_id', 'funding_id', 'amount_requested', 'status']):
        return jsonify({'message': 'Missing required fields!'}), 400

    funding_application = FundingApplication(
        user_id=data['user_id'],
        funding_id=data['funding_id'],
        amount_requested=data['amount_requested'],
        status=data['status']
    )
    db.session.add(funding_application)
    db.session.commit()
    return jsonify({'message': 'Funding application created successfully!', 'id': funding_application.id}), 201

@app.route('/funding_applications', methods=['GET'])
def get_funding_applications():
    funding_applications = FundingApplication.query.all()
    return jsonify([
        {
            'id': fa.id,
            'user_id': fa.user_id,
            'funding_id': fa.funding_id,
            'amount_requested': fa.amount_requested,
            'status': fa.status
        } for fa in funding_applications
    ]), 200

@app.route('/funding_applications/<int:id>', methods=['GET'])
def get_funding_application(id):
    funding_application = FundingApplication.query.get(id)
    if funding_application:
        return jsonify({
            'id': funding_application.id,
            'user_id': funding_application.user_id,
            'funding_id': funding_application.funding_id,
            'amount_requested': funding_application.amount_requested,
            'status': funding_application.status
        }), 200
    return jsonify({'message': 'Funding Application not found!'}), 404

@app.route('/funding_applications/<int:id>', methods=['PUT'])
def update_funding_application(id):
    funding_application = FundingApplication.query.get(id)
    if not funding_application:
        return jsonify({'message': 'Funding Application not found!'}), 404

    data = request.get_json()
    if 'amount_requested' in data:
        funding_application.amount_requested = data['amount_requested']
    if 'status' in data:
        funding_application.status = data['status']

    db.session.commit()
    return jsonify({'message': 'Funding Application updated successfully!'}), 200

@app.route('/funding_applications/<int:id>', methods=['DELETE'])
def delete_funding_application(id):
    funding_application = FundingApplication.query.get(id)
    if funding_application:
        db.session.delete(funding_application)
        db.session.commit()
        return jsonify({'message': 'Funding Application deleted successfully!'}), 200
    return jsonify({'message': 'Funding Application not found!'}), 404
