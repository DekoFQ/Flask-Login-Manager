from flask import Blueprint, redirect, render_template,url_for, request
from forms import Login
from flask_login import login_user
from models import User
from extentions import db
import bcrypt


blpl = Blueprint("loginApp", __name__, template_folder="./templates", static_folder="./static")




@blpl.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()

    if form.validate_on_submit():

        user = db.usuarios.find_one({"name":form.name.data})
        new_user = User(user)


        if user:
            hash_password = user.get('password')

            if hash_password and bcrypt.checkpw(form.password.data.encode('utf-8'), hash_password):

                 login_user(new_user)
                 return redirect(url_for('appDash.dashboard'))
            
    return render_template('login.html', form=form)