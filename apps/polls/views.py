from flask import Blueprint
from flask import render_template, redirect, session

from apps.polls.forms import ProfileForm, EvaluationForm
from apps.polls.models import Profile, Experiment, ProfileExperiment, EvaluationExperiment
from apps.polls.models.experiment_model import ExperimentStatusEnum
from utils import db

poll = Blueprint('poll', __name__, url_prefix='/')


@poll.route('/', methods=('GET', 'POST'))
def index():
    form = ProfileForm()
    if form.validate_on_submit():
        try:
            profile = Profile(
                user_gender=form.data.get('user_gender'),
                user_age=form.data.get('user_age')
            )
            profile.save()
            session['profile_id'] = profile.id
            return redirect('/information')
        except Exception as e:
            print(f'ERROR: {e}')
    return render_template('/polls/index.html', **locals())


@poll.route('/information', methods=('GET',))
def experiment_information():
    return render_template('/polls/experiment_information.html', **locals())


@poll.route('/experiments', methods=('GET',))
def experiments():
    experiment_list = Experiment.query.all()
    return render_template('/polls/experiments.html', **locals())


@poll.route('/experiments/<int:experiment_id>/ready', methods=('GET',))
def experiment_ready(experiment_id):
    current_profile_id = session['profile_id']
    try:
        if not session.get('profile_experiment'):
            profile_experiment = ProfileExperiment(
                profile_id=current_profile_id,
                experiment_id=experiment_id,
                status=ExperimentStatusEnum.new
            )
            db.session.add(profile_experiment)
            db.session.commit()
            session['profile_experiment'] = profile_experiment.id
        else:
            profile_experiment = ProfileExperiment.get_by_id(session.get('profile_experiment'))
            profile_experiment.status = ExperimentStatusEnum.repeat
            profile_experiment.update()
    except Exception as e:
        print(f'ERROR: {e}')

    return render_template('/polls/experiment_ready.html', **locals())


@poll.route('/experiments/<int:experiment_id>/running', methods=('GET',))
def experiment_running(experiment_id):
    current_p_exp_id = session['profile_experiment']
    try:
        p_exp = ProfileExperiment.get_by_id(current_p_exp_id)
        p_exp.status = ExperimentStatusEnum.running
        p_exp.update()
    except Exception as e:
        print(f'ERROR: {e}')
    return render_template('/polls/experiment_running.html', **locals())


@poll.route('/experiments/<int:experiment_id>/finished', methods=('GET', 'POST'))
def experiment_finished(experiment_id):
    current_p_exp_id = session['profile_experiment']
    try:
        p_exp = ProfileExperiment.get_by_id(current_p_exp_id)
        p_exp.status = ExperimentStatusEnum.finished
        p_exp.update()
    except Exception as e:
        print(f'ERROR: {e}')
    return render_template('/polls/experiment_finished.html', **locals())


@poll.route('/experiments/<int:experiment_id>/stopped', methods=('GET', 'POST'))
def experiment_stopped(experiment_id):
    current_p_exp_id = session['profile_experiment']
    try:
        p_exp = ProfileExperiment.get_by_id(current_p_exp_id)
        p_exp.status = ExperimentStatusEnum.stopped
        p_exp.update()
    except Exception as e:
        print(f'ERROR: {e}')
    return render_template('/polls/experiment_stopped.html', **locals())


@poll.route('/experiments/<int:experiment_id>/evaluation', methods=('GET', 'POST'))
def experiment_evaluation(experiment_id):
    form = EvaluationForm()
    current_p_exp_id = session['profile_experiment']
    if form.validate_on_submit():
        try:
            evaluation_exp = EvaluationExperiment(
                happy_rate=form.data.get('happy_rate'),
                mood_rate=form.data.get('mood_rate'),
                description=form.data.get('description'),
                experiment_id=experiment_id
            )
            evaluation_exp.p_id = current_p_exp_id
            evaluation_exp.save()
            return redirect(f'/experiments/{experiment_id}/thanks')
        except Exception as e:
            print(f'ERROR: {e}')
    return render_template('/polls/experiment_evaluation.html', **locals())


@poll.route('/experiments/<int:experiment_id>/thanks', methods=('GET', 'POST'))
def experiment_thanks(experiment_id):
    session.pop('profile_experiment')
    return render_template('/polls/experiment_thanks.html', **locals())


@poll.route('/finished', methods=('GET',))
def finished():
    return render_template('/polls/finished.html', **locals())


@poll.route('/stopped', methods=('GET',))
def stopped():
    return render_template('/polls/stopped.html', **locals())
