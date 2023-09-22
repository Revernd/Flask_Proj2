from flask import (
    Flask, render_template,
    request, make_response,session,
    url_for, redirect)
from flask_sqlalchemy import SQLAlchemy
from flask.views import View
from sample_blueprint import sampleBP
import click
from flask.cli import AppGroup
import os


app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SECRET_KEY'] = 'any random string value'
db = SQLAlchemy(app)
app.register_blueprint(sampleBP)


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
        from models import User, Contact, Blogpost, Tag
        db.create_all()

        app.cli.add_command(mycommand)
        app.cli.add_command(group_cli)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    app.register_blueprint(sampleBP)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, AppFactory!'
    return app


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
    return '<h1>Hello World!!</h1>'


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


@app.route('/getcookie/')
def getcookie():
    usercount = request.cookies.get('usercount')
    return "Value of 'usercount' cookie is : " + str(usercount)


@app.route('/setcookie/')
def setcookie():
    nusers = User.query.count()
    resp = make_response("<h2> 'usercount' cookie is sucessfully set.</h2>")
    resp.set_cookie('usercount', str(nusers))
    return resp


@app.route('/index/')
def index():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + \
            "<b><a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/login'></b>" + \
        "click here to log in</b></a>"


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        user = User(request.form['username'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return '''
    <form action="" method="post">
        <p>User Name : <input type='text' name='username'/></p>
        <p><input type='submit' value='Login'/></p>
    </form>
    '''


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)
