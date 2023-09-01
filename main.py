from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
import os
import mistune
import time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

if not os.path.exists("pages"):
    os.makedirs("pages")


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')
            return render_template('login.html')
    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already taken')
            return render_template('signup.html')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
    return render_template('signup.html')


@app.route("/profile/<username>")
@login_required
def profile(username):
    return render_template("profile.html", username=username)


@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    filename = (
        request.form.get("filename")
        or request.form.get("post_name")
        or f"{time.time()}.md"
    )
    if not os.path.exists("pages"):
        os.makedirs("pages")
    with open(os.path.join("pages", filename), "w") as f:
        f.write(request.form.get("markdown"))
    return redirect(url_for("page", filename=filename))


def load_and_parse_md(filename):
    with open(os.path.join("pages", filename)) as f:
        markdown_content = f.read()
    html_content = mistune.markdown(markdown_content)
    return html_content


@app.route("/page/<filename>")
def page(filename):
    html_content = load_and_parse_md(filename)
    return html_content


if __name__ == "__main__":
    app.run(debug=True)
