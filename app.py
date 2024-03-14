from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from flask_gravatar import Gravatar
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, BlogPost, Comment
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from extensions import db


"""-----------------------------------APP CONFIG------------------------------------------"""

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
ckeditor = CKEditor(app)
Bootstrap5(app)

"""----------------------------------FLASK LOGIN CONFIG--------------------------------------"""

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


"""----------------------------------------INIT DATA BASE----------------------------------------"""

db.init_app(app)

with app.app_context():
    db.create_all()

"""-------------------------------GRAVATAR CONFIG-------------------------------------------------"""

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

"""----------------------------------DECORATORS---------------------------------------------------------"""


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        with app.app_context():
            if current_user.is_authenticated and current_user.id == 1:
                return f(*args, **kwargs)
            else:
                abort(403)

    return decorated_function


"""---------------------------------APP ROUTES---------------------------------------------------------"""


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        with app.app_context():
            email = form.email.data

            result = db.session.execute(db.select(User).where(User.email == email))
            user = result.scalar()

            if user:
                flash("You've already signed up with that email, log in instead!", 'error')
                return redirect(url_for('login'))
            else:
                hash_and_salted_password = generate_password_hash(
                    password=form.password.data,
                    method='pbkdf2:sha256',
                    salt_length=8
                )

                new_user = User(
                    name=form.name.data,
                    email=form.email.data,
                    password=hash_and_salted_password

                )

                db.session.add(new_user)
                db.session.commit()

                login_user(new_user)

                return redirect(url_for('get_all_posts'))

    return render_template("register.html", form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        with app.app_context():
            email = form.email.data
            password = form.password.data

            result = db.session.execute(db.select(User).where(User.email == email))
            user = result.scalar()

            if not user:
                flash("The email does not exist, please try again or register.", 'error')
                return redirect(url_for('login'))
            elif not check_password_hash(user.password, password):
                flash('Password incorrect, please try again.')
                return redirect(url_for('login'))
            else:
                login_user(user)
                return redirect(url_for('get_all_posts'))

    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have successfully logged out!", "success")
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()

    return render_template("index.html", all_posts=posts, current_user=current_user)


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = CommentForm()
    requested_post = db.get_or_404(BlogPost, post_id)

    if form.validate_on_submit():

        if not current_user.is_authenticated:
            flash("You need to log in or register to comment.", 'error')
            return redirect(url_for('login'))

        else:

            new_comment = Comment(
                comment_author=current_user,
                parent_post=requested_post,
                text=form.body.data
            )

            db.session.add(new_comment)
            db.session.commit()

            return redirect(url_for('show_post', post_id=post_id))

    return render_template("post.html", post=requested_post, current_user=current_user, form=form)


@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            author_id=current_user.id,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, current_user=current_user)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True, current_user=current_user)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
