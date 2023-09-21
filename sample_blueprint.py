from flask import Blueprint, render_template

sampleBP = Blueprint(
    'sample',
    __name__,
    template_folder='templates/sample',
    static_folder='static/sample',
    url_prefix="/sample"
)


@sampleBP.route('/')
def home():
    return render_template('home.html')