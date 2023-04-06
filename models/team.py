from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from ..database import db
from .employee import Employee

class Team(db.Model):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    team_lead = Column(Integer, ForeignKey("employees.id"), nullable=False)

    lead = relationship("Employee", foreign_keys=[team_lead])
    members = relationship(lambda: Employee, back_populates="team", foreign_keys=[Employee.team_id])

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
