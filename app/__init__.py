from flask import Flask, render_template
# from flask_mysql_connector import MySQL
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY
# from flask_wtf.csrf import CSRFProtect

# mysql = MySQL()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['MYSQL_HOST'] = DB_HOST
    app.config['MYSQL_USER'] = DB_USERNAME
    app.config['MYSQL_PASSWORD'] = DB_PASSWORD
    app.config['MYSQL_DATABASE'] = DB_NAME

    # mysql.init_app(app)

    @app.route("/")
    def index():
        return render_template('base.html')

    from app.routes.admin import admin_bp
    from app.routes.doctor import doctor_bp
    from app.routes.medtech import medtech_bp
    from app.routes.receptionist import receptionist_bp
    
    app.register_blueprint(admin_bp, url_prefix='/admin/')
    app.register_blueprint(doctor_bp, url_prefix='/doctor/')
    app.register_blueprint(medtech_bp, url_prefix='/medtech/')
    app.register_blueprint(receptionist_bp, url_prefix='/receptionist/')

    return app