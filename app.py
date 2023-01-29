from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(20), nullable=False, default='profile.jpg')
    email = db.Column(db.String(200), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


posts = [
    {
        'autor': 'Jhon Doe',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2023'
    },
    {
        'autor': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2023'
    },
    {
        'autor': 'Victor Doe',
        'title': 'Blog Post 3',
        'content': 'Third post content',
        'date_posted': 'April 22, 2023'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@localhost.com' and form.password.data == 'Password-123':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


with app.app_context():
    db.create_all()
    db.drop_all()
    db.create_all()

    user1 = User(username='victor', email="victor@localhost.com", password="Password-123")
    user2 = User(username='jhon', email="jhon@localhost.com", password="Password-123")
    user3 = User(username='bob', email="bob@localhost.com", password="Password-123")
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

    post1 = Post(title='Blog Post 1', content='First post content', author=user1)
    post2 = Post(title='Blog Post 2', content='Second post content', author=user2)
    post3 = Post(title='Blog Post 3', content='Third post content', author=user3)
    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)
    db.session.commit()

    print(User.query.all())
    print(Post.query.all())

if __name__ == '__main__':
    app.run(debug=True)
