from enum import Enum
from typing import List

from utils import db


class Gender(Enum):
    male = 'male'
    female = 'female'


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer(), primary_key=True)
    user_gender = db.Column(db.Enum(Gender), nullable=False)
    user_age = db.Column(db.Integer, nullable=False)
    p_exps = db.relationship('ProfileExperiment', backref='p_exps', lazy=True)

    def __repr__(self):
        return f'<Session: {self.id}|{self.user_gender}|{self.user_age}>'

    def __str__(self):
        return f'Session: {self.id}|{self.user_gender}|{self.user_age}'

    @classmethod
    def filter_by_user_gender(cls, user_gender: Gender) -> List['Profile']:
        return cls.query.filter_by(user_gender=user_gender).all()

    @classmethod
    def filter_by_user_age(cls, user_age: int) -> List['Profile']:
        return cls.query.filter_by(user_age=user_age).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
