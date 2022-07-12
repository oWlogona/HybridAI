from typing import List

from utils import db


class EvaluationExperiment(db.Model):
    __tablename__ = 'evaluation_experiment'

    id = db.Column(db.Integer(), primary_key=True)
    happy_rate = db.Column(db.Integer, nullable=False)
    mood_rate = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text(), nullable=True)
    p_id = db.Column(db.Integer(), db.ForeignKey('profile.id'), nullable=False)
    experiment_id = db.Column(db.Integer(), db.ForeignKey('experiment.id'), nullable=False)

    def __repr__(self):
        return f'<EvaluationExperiment: {self.id}|{self.happy_rate}|{self.mood_rate}>'

    def __str__(self):
        return f'EvaluationExperiment: {self.id}|{self.happy_rate}|{self.mood_rate}'

    @classmethod
    def filter_by_happy_rate(cls, happy_rate: int) -> List['EvaluationExperiment']:
        return cls.query.filter_by(happy_rate=happy_rate).all()

    @classmethod
    def filter_by_mood_rate(cls, mood_rate: int) -> List['EvaluationExperiment']:
        return cls.query.filter_by(mood_rate=mood_rate).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
