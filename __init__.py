import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .commands import mycommand, group_cli

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_path='/path/to/project')
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'Project/mydatabase.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    db.init_app(app)

    @app.shell_context_processor
    def make_shell_context():
        return dict(app=app, db=db)

    with app.app_context():
        from .models import User, Contact, Blogpost, Tag
        db.create_all()

        app.cli.add_command(mycommand)
        app.cli.add_command(group_cli)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import app, sample_blueprint

    app.register_blueprint(app.helloBP)
    app.register_blueprint(sample_blueprint.sampleBP)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, AppFactory!'

    return app