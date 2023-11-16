from flask import Blueprint, redirect, url_for, render_template, make_response
from flask_login import logout_user, login_required, current_user


blpo = Blueprint("appLogout", __name__, template_folder="./templates", static_folder="./static")


@blpo.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()

    return redirect(url_for('loginApp.login'))


