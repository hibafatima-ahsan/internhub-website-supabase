from flask import Flask, render_template
from config import Config
from routes.main import main_bp
from routes.auth import auth_bp
from routes.internships import internships_bp
from routes.student import student_bp
from routes.company import company_bp
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(internships_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', content="<div class='hero'><h2>404 - Page Not Found</h2><p>The requested page could not be located.</p></div>"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('base.html', content="<div class='hero'><h2>500 - Internal Server Error</h2><p>An unexpected server error occurred.</p></div>"), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
