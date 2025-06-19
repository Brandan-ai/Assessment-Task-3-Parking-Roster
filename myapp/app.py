from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from .extensions import db, login_manager, migrate

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager.login_view = 'login'

def init_routes(app):
    from .models import User, Spot

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                login_user(user)  # Logs in the user using Flask-Login
                return redirect(url_for('home'))
            else:
                flash('Login failed. Check your username and password.')

        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

            new_user = User(username=username, email=email)
            new_user.set_password(password)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Registered successfully! You can now log in.')
                return redirect(url_for('login'))
            except IntegrityError:
                db.session.rollback()
                flash('Username or email already exists.')
        return render_template('register.html')

    @app.route('/home')
    @login_required
    def home():
        return render_template('home.html',
        username = current_user.username)

    @app.route('/parking', methods=['POST', 'GET'])
    def select_number():
        button_pressed = request.form.get('button')  # from homepage buttons
        selected_number = None

        if request.method == 'POST':
            selected_number = request.form.get('number')
            
            if selected_number:
                selected_number = int(selected_number)

                # Check if the parking spot exists
                existing_spot = Spot.query.filter_by(position=selected_number, day=button_pressed).first()
                day=button_pressed
                if existing_spot:
                    flash("That spot is already taken for this day.", "warning")
                else:
                    # Create Spot record
                    new_spot = Spot(
                        position=selected_number,
                        user_id=current_user.id,
                        avaliable=False,
                        day=day
                    )
                    db.session.add(new_spot)
                    db.session.commit()
                    flash("Parking spot reserved!", "success")

        return render_template('parking.html', result=button_pressed, selected_number=selected_number)



    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Logged out successfully.')
        return redirect(url_for('login'))
