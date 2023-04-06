from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship, backref
from ..database import db


class Employee(db.Model):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    phone_number = Column(String, nullable=False)
    company = Column(String, nullable=False)
    lcat = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    termination_date = Column(Date, nullable=True)
    is_team_lead = Column(Boolean, default=False)

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = relationship("Team", back_populates="members", foreign_keys=[team_id])

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
