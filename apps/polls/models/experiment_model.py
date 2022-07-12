from enum import Enum
from typing import List

from utils import db


class ExperimentStatusEnum(Enum):
    new = 'new'
    repeat = 'repeat'
    running = 'running'
    finished = 'finished'
    stopped = 'stopped'
    failed = 'failed'


class Experiment(db.Model):
    __tablename__ = 'experiment'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    pattern_id = db.Column(db.String(75), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False, default=True)
    profile_experiments = db.relationship('ProfileExperiment', backref='p_experiment', lazy=True)

    def __repr__(self):
        return f'<Experiment: {self.id}|{self.pattern_id}>'

    def __str__(self):
        return f'Experiment: {self.id}|{self.pattern_id}'

    @classmethod
    def filter_by_pattern_id(cls, pattern_id: str) -> List['Experiment']:
        return cls.query.filter_by(pattern_id=pattern_id).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class ProfileExperiment(db.Model):
    __tablename__ = 'profile_experiment'

    id = db.Column(db.Integer(), primary_key=True)
    profile_id = db.Column(db.Integer(), db.ForeignKey('profile.id'), nullable=False)
    experiment_id = db.Column(db.Integer(), db.ForeignKey('experiment.id'), nullable=False)
    status = db.Column(db.Enum(ExperimentStatusEnum), nullable=False)

    def __repr__(self):
        return f'<ProfileExperiment: {self.id}|{self.profile_id}|{self.experiment_id}|{self.status}>'

    def __str__(self):
        return f'ProfileExperiment: {self.id}|{self.profile_id}|{self.experiment_id}|{self.status}'

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
