import unittest
from datetime import datetime

from flask_testing import TestCase
from app import app, db
from models import Employee


class TestModels(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_employees.db'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_employee_creation(self):
        # Given
        employee = Employee(name="John Doe", email="john.doe@example.com", phone_number="555-555-5555",
                            company="ACME corp", lcat="SWE 3", assigned_team="Team A",
                            start_date=datetime.today(), is_team_lead=False)

        # When
        db.session.add(employee)
        db.session.commit()

        # Then
        self.assertIsNotNone(employee.id)
        self.assertEqual(employee.name, "John Doe")
        self.assertEqual(employee.email, "john.doe@example.com")
        self.assertEqual(employee.phone_number, "555-555-5555")
        self.assertEqual(employee.company, "ACME corp")
        self.assertEqual(employee.lcat, "SWE 3")
        self.assertEqual(employee.assigned_team, "Team A")
        self.assertEqual(employee.is_team_lead, False)

    # Add more test cases for your Employee model here


if __name__ == '__main__':
    unittest.main()