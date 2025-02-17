import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Import database and extensions
from models.models import db
from utils.extensions import limiter

# Load environment variables
load_dotenv()

def create_app():
	"""Factory function to create and configure the Flask application."""
	app = Flask(__name__)

	# Database Configuration
	app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///libvault.db')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	# JWT Configuration (No need to set expiration here, handled in api.auth)
	app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')

	# Rate Limiting Storage
	app.config.setdefault('RATELIMIT_STORAGE_URI', 'memory://')

	# Initialize Extensions
	db.init_app(app)
	limiter.init_app(app)
	migrate = Migrate(app, db)
	jwt = JWTManager(app)

	# CORS Configuration (Allows frontend access)
	CORS(
		app,
		resources={r"/*": {
			"origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
			"methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
			"allow_headers": ["Content-Type", "Authorization"]
		}},
		supports_credentials=True
	)

	@app.before_request
	def handle_options():
		"""Handle preflight OPTIONS requests to prevent CORS issues."""
		if request.method == 'OPTIONS':
			return '', 200

	# ----------------- REGISTER BLUEPRINTS ----------------- #
	from api.routes import routes
	from api.articles import articles_bp
	from api.auth import auth_bp

	app.register_blueprint(auth_bp, url_prefix='/api/auth')
	app.register_blueprint(articles_bp, url_prefix='/api/auth')
	app.register_blueprint(routes)

	# ----------------- HEALTH CHECK ROUTE ----------------- #
	@app.route('/health', methods=['GET'])
	def health_check():
		"""Simple route to check if the API is running."""
		return jsonify({"status": "ok", "message": "LibVault API is running"}), 200

	return app


if __name__ == '__main__':
	app = create_app()

	# Ensure database tables are created
	with app.app_context():
		try:
			db.create_all()
			print("Database initialized successfully.")
		except Exception as e:
			print(f"Error initializing database: {e}")

	# Start the Flask server
	app.run(debug=True)
