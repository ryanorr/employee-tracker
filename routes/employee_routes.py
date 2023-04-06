# routes/employee_routes.py

from flask import request, jsonify
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime
from ..models.employee import Employee


class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        load_instance = True

    termination_date = fields.Date(allow_none=True)


employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


def register_employee_routes(app, db):
    @app.route('/api/employees', methods=['GET'])
    def get_all_employees():
        employees = Employee.query.all()
        return jsonify([employee.to_dict() for employee in employees])

    @app.route('/api/employees', methods=['POST'])
    def create_employee():
        data = request.get_json()

        date_fields = ['start_date', 'termination_date']
        data.update(
            {field: datetime.strptime(data.get(field), '%Y-%m-%d').date() if data.get(field) else None for field in
             date_fields})

        new_employee = Employee(**data)
        db.session.add(new_employee)
        db.session.commit()

        return jsonify(employee_schema.dump(new_employee)), 201

    @app.route('/api/employees/<int:employee_id>', methods=['PUT'])
    def update_employee(employee_id):
        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        data = request.get_json()
        date_fields = ['start_date', 'termination_date']

        for key, value in data.items():
            if key in date_fields and value is not None:
                value = datetime.strptime(value, '%Y-%m-%d').date()
            setattr(employee, key, value)

        db.session.commit()

        return jsonify(employee_schema.dump(employee)), 200

    @app.route('/api/employees/<int:employee_id>', methods=['GET'])
    def get_employee(employee_id):
        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        return jsonify(employee_schema.dump(employee)), 200

    @app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
    def delete_employee(employee_id):
        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        db.session.delete(employee)
        db.session.commit()

        return jsonify({"message": "Employee deleted"}), 200