import flask
from flask import render_template
from flask import request, url_for, redirect
from flask_login import login_user, logout_user, login_required

from applications.forms import *
from main import app, bcrypt


@app.route("/home", methods=["GET"])
@app.route('/', methods=["GET"])
def indexPage():
    if not session.get('acc_type'):
        session['acc_type'] = None
    users = User.query.all()
    venues = Venue.query.all()
    shows = Shows.query.all()
    if current_user.is_authenticated:
        if session['acc_type'] == 'Admin':
            return render_template("admin_dash.html", venues=venues, shows=shows)
        return render_template("booking.html", users=users, venues=venues, shows=shows)
    else:
        return render_template("booking.html", users=users, venues=venues, shows=shows)


@app.route('/Userlogin', methods=["GET", "POST"])
def Userlogin():
    form = Login(request.form)
    if current_user.is_authenticated and session['acc_type'] == 'User':
        flask.flash("Already Logged in! You can use the site now", "info")
        return redirect(url_for('indexPage'))
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flask.flash("Login Successful", "success")
                session['acc_type'] = 'User'
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for('indexPage'))
            else:
                flask.flash("Login Unsuccessful, Please check Email and password", 'danger')
    return render_template("user_login.html", form=form)


@app.route('/UserReg', methods=["GET", "POST"])
def UserReg():
    if current_user.is_authenticated and session['acc_type'] == 'User':
        flask.flash("Already Logged in! You can use the site now", "info")
        return redirect(url_for('indexPage'))

    form = Registration(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            psw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=psw_hash)
            session['acc_type'] = 'User'
            db.session.add(user)
            db.session.commit()
            flask.flash(f"Account Created for {form.username.data}. You can Login now", "success")
            return redirect(url_for("indexPage"))
    return render_template("user_register.html", form=form)


@app.route('/Adminlogin', methods=["GET", "POST"])
def Adminlogin():
    form = Login(request.form)
    if current_user.is_authenticated and session['acc_type'] == 'Admin':
        flask.flash("Already Logged in! You can use the site now", "info")
        return redirect(url_for('indexPage'))
    if request.method == "POST":
        if form.validate_on_submit():
            admin = Admin.query.filter_by(email=form.email.data).first()
            if admin and (admin.password == form.password.data):
                session['acc_type'] = 'Admin'
                login_user(admin, remember=form.remember.data)
                flask.flash("Admin Login Successful", "success")
                return redirect(url_for('indexPage'))
            else:
                flask.flash("Login Unsuccessful, Please check Email and password", 'danger')
    return render_template("admin_login.html", form=form)


@app.route("/rate/<int:show_id>", methods=["GET", "POST"])
@login_required
def rateShow(show_id):
    form = RateShow(request.form)
    show = Shows.query.filter_by(show_id=show_id).first()
    if request.method == "POST":
        if form.validate_on_submit():
            show.show_rating = (int(show.show_rating) + int(form.rate.data)) / (int(show.num_rating) + 1)
            show.num_rating = show.num_rating + 1
            db.session.commit()
            flask.flash("You have rated the show", 'success')
            return redirect(url_for('indexPage'))
    return render_template("rate_show.html", form=form, show=show)


@app.route('/myBookings', methods=["GET"])
@login_required
def myBookings():
    if not current_user.is_authenticated:
        return redirect(url_for("indexPage"))
    user = User.query.get(int(current_user.get_id()))
    return render_template("my_bookings.html", shows=user.bookings, venues=Venue.query.all())


@app.route("/booking/<int:show_id>", methods=["GET", "POST"])
@login_required
def bookShows(show_id):
    form = BookShow(request.form)
    user = User.query.filter_by(user_id=current_user.user_id).first()
    show = Shows.query.filter_by(show_id=show_id).first()
    if request.method == "POST":
        if form.validate_on_submit():
            show.show_current = show.show_current + form.seats.data
            db.session.add(Reservation(user_id=user.user_id, show_id=show.show_id, num_seats=form.seats.data))
            db.session.commit()
            return redirect(url_for('indexPage'))
    return render_template("book_show.html", form=form, show=show)


@app.route("/booking/<int:show_id>/delete", methods=["GET", "POST"])
@login_required
def deleteBooking(show_id):
    show = Shows.query.filter_by(show_id=show_id).first()
    reservation = Reservation.query.filter_by(user_id=current_user.get_id(), show_id=show.show_id).first()
    db.session.delete(reservation)
    db.session.commit()
    flask.flash(f"Reservation has been deleted", 'warning')
    return redirect(url_for('indexPage'))


@app.route('/show/<int:venue_id>/new', methods=["GET", "POST"])
@login_required
def newshow(venue_id):
    if session['acc_type'] == 'User' or not current_user.is_authenticated:
        flask.flash("Page is for Admins only! Do not access", "danger")
        return redirect(url_for("indexPage"))
    form = NewShow(request.form)
    if request.method == "POST":
        if form.validate():
            show = Shows(show_name=form.name.data, show_price=form.price.data, show_desc=form.desc.data,
                         show_date=form.datetime.data, show_cap=form.cap.data, show_venue=venue_id)
            db.session.add(show)
            flask.flash(f"Show {show.show_name} has been created!", 'success')
            db.session.commit()
            return redirect(url_for('indexPage'))
    return render_template("new_show.html", form=form, legend="New Show")


@app.route("/show/<int:show_id>/edit", methods=["GET", "POST"])
@login_required
def editShow(show_id):
    if session['acc_type'] == 'User' or not current_user.is_authenticated:
        flask.flash("Page is for Admins only! Do not access", "danger")
        return redirect(url_for("indexPage"))
    show = Shows.query.filter_by(show_id=show_id).first()
    form = EditShow(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            show.show_name = form.name.data
            show.show_desc = form.desc.data
            show.show_price = form.price.data
            show.show_date = form.datetime.data
            show.show_cap = form.cap.data
            show.show_current = form.current_cap.data
            db.session.commit()
            flask.flash("Show has been updated!", 'success')
            return redirect(url_for('indexPage'))
    elif request.method == "GET":
        form.name.data = show.show_name
        form.desc.data = show.show_desc
        form.price.data = show.show_price
        form.datetime.data = show.show_date
        form.cap.data = show.show_cap
        form.current_cap.data = show.show_current
    return render_template("new_show.html", form=form, legend="Update Show")


@app.route("/show/<int:show_id>/delete", methods=["GET", "POST"])
@login_required
def deleteShow(show_id):
    if session['acc_type'] == 'User' or not current_user.is_authenticated:
        flask.flash("Page is for Admins only! Do not access", "danger")
        return redirect(url_for("indexPage"))
    show = Shows.query.filter_by(show_id=show_id).first()
    show.bookings = []
    db.session.delete(show)
    db.session.commit()
    flask.flash(f"Show has been deleted", 'warning')
    return redirect(url_for('indexPage'))


@app.route("/newVenue", methods=["GET", "POST"])
@login_required
def newVenue():
    if session['acc_type'] == 'User' or not current_user.is_authenticated:
        flask.flash("Page is for Admins only! Do not access")
        return redirect(url_for("indexPage"))
    form = NewVenue(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            venue = Venue(venue_name=form.name.data, venue_loc=form.loc.data, venue_cap=form.cap.data)
            db.session.add(venue)
            db.session.commit()
            flask.flash(f"Venue {venue.venue_name} has been created!", 'success')
            return redirect(url_for('indexPage'))
    return render_template("new_venue.html", form=form, legend="Create Venue")


@app.route("/venue/<int:venue_id>/edit", methods=["GET", "POST"])
@login_required
def editVenue(venue_id):
    if session['acc_type'] == 'User' or not current_user.is_authenticated:
        flask.flash("Page is for Admins only! Do not access")
        return redirect(url_for("indexPage"))
    venue = Venue.query.filter_by(venue_id=venue_id).first()
    form = EditVenue(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            venue.venue_name = form.name.data
            venue.venue_loc = form.loc.data
            venue.venue_cap = form.cap.data
            db.session.commit()
            flask.flash(f"Venue {venue.venue_name} has been updated!", 'success')
            return redirect(url_for('indexPage'))
    elif request.method == "GET":
        form.name.data = venue.venue_name
        form.loc.data = venue.venue_loc
        form.cap.data = venue.venue_cap
    return render_template("new_venue.html", form=form, legend="Update Venue")


@app.route("/venue/<int:venue_id>/delete", methods=["GET", "POST"])
@login_required
def deleteVenue(venue_id):
    if session['acc_type'] == 'User' or not current_user.is_authenticated:
        flask.flash("Page is for Admins only! Do not access")
        return redirect(url_for("indexPage"))
    venue = Venue.query.filter_by(venue_id=venue_id).first()
    if venue.venue_shows is None:
        flask.flash("The Venue still has Shows! Delete the shows first")
        return redirect(url_for("indexPage"))
    else:
        db.session.delete(venue)
        db.session.commit()
        flask.flash("Venue has been deleted", 'warning')
        return redirect(url_for("indexPage"))


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    flask.flash("Logged Out", "success")
    session['acc_type'] = None
    return redirect(url_for("indexPage"))
