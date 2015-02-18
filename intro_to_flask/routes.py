from intro_to_flask import app, login_manager
from flask_login import login_user, login_required, logout_user, current_user
from flask import render_template, request, flash, session, redirect, url_for
from forms import ContactForm, SignupForm, SigninForm
from flask_mail import Message, Mail
from models import db, User
# from functools import wraps

# create login_required decorator
# def login_required(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'email' in session:
#             return f(*args, **kwargs)
#         else:
#             return redirect(url_for('signin'))
#
#     return wrap

mail = Mail()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    form = ContactForm()

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required')
            return render_template('contact.html', form=form)

        else:
            msg = Message(form.subject.data, sender='princechilas@gmail.com',
                          recipients=['iamchilas@live.com'])
            msg.body = """
            From: %s &lt;%s&gt;
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)

            return render_template('contact.html', success=True)

    elif request.method == 'GET':
        return render_template('contact.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' not in session:
        form = SignupForm()

        if request.method == 'POST':
            if not form.validate():
                return render_template('signup.html', form=form)
            else:
                new_user = User(form.firstname.data, form.lastname.data,
                                form.email.data, form.password.data)
                db.session.add(new_user)
                db.session.commit()

                session['email'] = new_user.email

                return redirect(url_for('profile'))

        elif request.method == 'GET':
            return render_template('signup.html', form=form)

    else:
        return redirect(url_for('profile'))


@app.route('/profile')
@login_required
def profile():

    # user = User.query.filter_by(user=session['email']).first()

    # if user is None:
    if current_user is None:
        return redirect(url_for('signin'))
    else:
        return render_template('profile.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if not login_manager.anonymous_user:
        return redirect(url_for(profile))

    form = SigninForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('signin.html', form=form)
        else:
            # session['email'] = form.email.data
            # user = User.query.filter_by(email=session['email']).first()
            user = User.query.filter_by(email=form.email.data).first()
            login_user(user, remember=True)
            return redirect(url_for('profile'))
    elif request.method == 'GET':
        return render_template('signin.html', form=form)


@app.route('/signout')
@login_required
def signout():
    # session.pop('email', None)
    logout_user()
    return redirect(url_for('home'))


# @app.error_handler(404)
# def page_not_found(e):
#     return redirect(url_for('home'))