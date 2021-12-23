from market import app, db
from flask import render_template, redirect, url_for, flash, request
from market.forms import ProfileForm, PurchaseItemForm, RegisterForm, LoginForm, SellItemForm
from market.sqlmodels import Items, Users
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route("/home/")
def home_page():
    return render_template('home.html')

@app.route("/market", methods=["GET","POST"])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()
    
    if request.method == 'POST':
        #purchase
        
        if purchase_form.validate_on_submit() and purchase_form.purchase.data:
            purchased_item = request.form.get('purchased_item')
            p_item = Items.query.filter_by(name=purchased_item).first()

            if p_item and current_user.can_purchase(p_item):
                p_item.buy(current_user)
                flash(message=f"congradulations! you have purchased {p_item.name}", category='success')
            else:
                flash(message="you cannot afford this item", category='danger')

        #sell

        if sell_form.validate_on_submit() and sell_form.sell.data:
            sold_item = request.form.get('sold_item')
            s_item = Items.query.filter_by(name=sold_item).first()

            if s_item and current_user.can_sell(s_item):
                s_item.sell(current_user)
                flash(message="sold this item", category='success')

        return redirect(url_for('market_page'))

    if request.method == 'GET':
        available_items = Items.query.filter_by(owner=None)
        owned_items = Items.query.filter_by(owner=current_user.id)

        return render_template('market.html', available_items=available_items,
                    purchase_form=purchase_form, owned_items=owned_items, sell_form=sell_form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm() # forms

    if form.validate_on_submit():
        attempt_user = Users.query.filter_by(username=form.username.data).first() #sql data
        
        if attempt_user and attempt_user.check_password_correction(
        attempted_password = form.password_1.data
        ):
            login_user(attempt_user)
            flash(message=f"you are logged in as {attempt_user.username}",
            category='success')
            return redirect(url_for("market_page"))
        else:
            flash(message="username or password does not match", category='danger')

    return render_template('login.html', form=form)

@app.route("/logout")
def logout_page():
    logout_user()
    flash(message="you have been successfully logged out", category='info')
    return redirect(url_for("home_page"))

@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = Users(username=form.username.data,
                               email_id=form.email_address.data,
                               password_hash=form.password_1.data)

        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(message=f"you are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))
    
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(message=err_msg, category='danger')
    
    return render_template('register.html', form=form)

@app.route("/user_profile", methods=["GET", "POST"])
@login_required
def user_profile():
    profile_change = ProfileForm()

    if profile_change.validate_on_submit():
        if current_user.check_password_correction(profile_change.password_1.data):
            current_user.add_budget(profile_change) 
        else:
            flash(message="your password is incorrect", category='danger')

    if profile_change.errors !={}:
        for err_msg in profile_change.errors.values():
            for err in err_msg:
                flash(message=f"{err}", category='danger')
    
    return render_template("profile.html", profile_change=profile_change)
