from app import db


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))
    contact = db.relationship(
        'Contact',
        backref='user',
        lazy=True,
        uselist=False
    )
    blogposts = db.relationship(
        'Blogpost',
        backref='user',
        lazy='dynamic'
    )

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<User '{}'>".format(self.username)


class Contact(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    city = db.Column(db.String(200))
    email = db.Column(db.String(100))
    phoneno = db.Column(db.String())
    userid = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    def __init__(self, city, email, phonenum):
        self.city = city
        self.email = email
        self.phoneno = phonenum


tags = db.Table('blogpost_tags',
    db.Column('blogpost_id', db.Integer, db.ForeignKey('blogpost.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class Blogpost(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(300))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    userid = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('blogposts', lazy='dynamic')
    )

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Blogpost '{}'>".format(self.title)


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    tagname = db.Column(db.String(255))

    def __init__(self, tagname):
        self.tagname = tagname

    def __repr__(self):
        return "<Tag '{}'>".format(self.tagname)
