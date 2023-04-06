from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from .database import db
from .routes.employee_routes import register_employee_routes
from .routes.team_routes import register_team_routes


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'*': {'origins': 'http://localhost:3000'}})

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    register_employee_routes(app, db)
    register_team_routes(app, db)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
