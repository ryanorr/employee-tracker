# routes/team_routes.py

from flask import request, jsonify
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.team import Team
from ..models.employee import Employee


class TeamSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        load_instance = True


team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)


def register_team_routes(app, db):
    @app.route('/api/teams', methods=['GET'])
    def get_all_teams():
        teams = Team.query.all()
        return jsonify([team.to_dict() for team in teams])

    @app.route('/api/teams', methods=['POST'])
    def create_team():
        data = request.get_json()
        new_team = Team(**data)
        db.session.add(new_team)
        db.session.commit()

        return jsonify(team_schema.dump(new_team)), 201

    @app.route('/api/teams/<int:team_id>', methods=['PUT'])
    def update_team(team_id):
        team = Team.query.get(team_id)
        if not team:
            return jsonify({"error": "Team not found"}), 404

        data = request.get_json()

        for key, value in data.items():
            setattr(team, key, value)

        db.session.commit()

        return jsonify(team_schema.dump(team)), 200

    @app.route('/api/teams/<int:team_id>', methods=['DELETE'])
    def delete_team(team_id):
        team = Team.query.get(team_id)
        if not team:
            return jsonify({"error": "Team not found"}), 404

        db.session.delete(team)
        db.session.commit()

        return jsonify(team_schema.dump(team)), 200

    @app.route('/api/teams/<int:team_id>/employees', methods=['GET'])
    def get_team_employees(team_id):
        team = Team.query.get(team_id)
        if not team:
            return jsonify({"error": "Team not found"}), 404

        return jsonify([employee.to_dict() for employee in team.employees])

    @app.route('/api/teams/<int:team_id>/employees', methods=['POST'])
    def add_team_employee(team_id):
        team = Team.query.get(team_id)
        if not team:
            return jsonify({"error": "Team not found"}), 404

        data = request.get_json()
        employee = Employee.query.get(data['employee_id'])
        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        team.employees.append(employee)
        db.session.commit()

        return jsonify(team_schema.dump(team)), 200
