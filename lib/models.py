from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    character_name = Column(String)

    # One role has many auditions
    auditions = relationship('Audition', backref='role')

    # List of actor names from all auditions for this role
    @property
    def actors(self):
        return [audition.actor for audition in self.auditions]

    # List of locations from all auditions for this role
    @property
    def locations(self):
        return [audition.location for audition in self.auditions]

    # First audition hired for this role (lead)
    def lead(self):
        hired_auditions = [a for a in self.auditions if a.hired]
        if hired_auditions:
            return hired_auditions[0]
        return 'no actor has been hired for this role'

    # Second audition hired for understudy
    def understudy(self):
        hired_auditions = [a for a in self.auditions if a.hired]
        if len(hired_auditions) > 1:
            return hired_auditions[1]
        return 'no actor has been hired for understudy for this role'


class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer, primary_key=True)
    actor = Column(String)
    location = Column(String)
    phone = Column(Integer)
    hired = Column(Boolean, default=False)

    role_id = Column(Integer, ForeignKey('roles.id'))

    # This method sets hired to True
    def call_back(self):
        self.hired = True
