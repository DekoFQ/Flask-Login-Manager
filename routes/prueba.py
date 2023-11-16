from flask import Blueprint, render_template


blpp = Blueprint("appPrueba", __name__, template_folder="./templates")


@blpp.route('/prueba')
def prueba():
    return render_template('prueba.html')