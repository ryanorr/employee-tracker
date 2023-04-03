from database import db


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(15), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    lcat = db.Column(db.String(50), nullable=False)
    assigned_team = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    termination_date = db.Column(db.Date, nullable=True)
    is_team_lead = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'company': self.company,
            'lcat': self.lcat,
            'assigned_team': self.assigned_team,
            'start_date': self.start_date.isoformat(),
            'termination_date': self.termination_date.isoformat() if self.termination_date else None,
            'is_team_lead': self.is_team_lead
        }
