# Web Survey App

It's an application where each user can run and rate different patterns on the local device.

## Setup Project on local machine

1. Install all required packages

```bash
pip install -r requirements.txt
```

2. Init flask variables

```bash
export FLAK_APP=run.py
export FLASK_ENV=development
```

3. Create database tables

```bash
flask shell
db.create_all() - (in flask shell)
exit() - (in flask shell)
```

4. Run flask server

```bash
flask run
```
