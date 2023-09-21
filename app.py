from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask.views import View
from sample_blueprint import sampleBP
import click
from flask.cli import AppGroup


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)
app.register_blueprint(sampleBP)


@click.command('command1')
@click.argument('name')
def mycommand(name):
    print(name)


group_cli = AppGroup('group1')


@group_cli.command('command1')
@click.argument('name')
def mycommand2(name):
    print(name)


def startswith(word, tag):
    if word.startswith(tag):
        return tag + '-word'
    return 'non-' + tag + '-word'


app.jinja_env.filters['startswith'] = startswith


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, x=25, y=65)

@app.route('/')
def hello_view():
    return '<h1>Hello World!!!</h1>'


class BaseView(View):
    def __init__(self, template_name):
        self.template = template_name
        super(BaseView, self).__init__()

    def dispatch_request(self):
        return render_template(self.template)

app.add_url_rule('/users/', view_func=BaseView.as_view('display_users', template_name='listusers.html'))


class ListView(BaseView):
    def __init__(self, template_name, model):
        self.model = model
        super(ListView, self).__init__(template_name)

    def get_objects(self):
        objects = self.model.query.all()
        return {self.model.__tablename__+'s':objects}

    def dispatch_request(self):
        return render_template(self.template, **self.get_objects())


from models import User
app.add_url_rule('/userlist/', view_func=ListView.as_view('show_users', template_name='listusers.html',  model=User))
