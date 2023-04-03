import unittest
from flask_testing import TestCase
from datetime import date
from app import app, db, Employee


def create_sample_employee():
    employee = Employee(
        name="Jane Smith",
        email="jane.smith@example.com",
        phone_number="555-555-1234",
        company="Acme Corp",
        lcat="Developer",
        assigned_team="Team B",
        start_date=date(2023, 1, 1),
        is_team_lead=True
    )
    db.session.add(employee)
    db.session.commit()
    return employee


class TestApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        with app.test_client() as self.app:
            self.app.testing = True
            with app.app_context():
                db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_employee(self):
        response = self.app.post('/api/employees', json={
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone_number": "555-555-5555",
            "company": "Acme Corp",
            "lcat": "Developer",
            "assigned_team": "Team A",
            "start_date": "2023-05-01",
            "is_team_lead": False
        })
        self.assertEqual(response.status_code, 201)

    def test_update_employee(self):
        employee = create_sample_employee()
        response = self.app.put(f'/api/employees/{employee.id}', json={
            "name": "Jane Smith Updated",
            "email": "jane.smith_updated@example.com",
            "phone_number": "555-555-5678",
            "company": "Acme Corp",
            "lcat": "Senior Developer",
            "assigned_team": "Team C",
            "start_date": "2023-01-01",
            "termination_date": "2023-05-01",
            "is_team_lead": False
        })
        self.assertEqual(response.status_code, 200)

    def test_get_employee(self):
        employee = create_sample_employee()
        response = self.app.get(f'/api/employees/{employee.id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_employee(self):
        employee = create_sample_employee()
        response = self.app.delete(f'/api/employees/{employee.id}')
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()