from flask import Flask,render_template
from flask_login import LoginManager, login_user
from extentions import db
from routes.register import blpr
from routes.login import blpl
from routes.dashboard import blpd
from routes.logout import blpo
from routes.prueba import blpp
from routes.prueba_vehiculo import blppv
from routes.vehiculos import blpv
from bson import ObjectId
from models import User




app = Flask(__name__)


app.config["SECRET_KEY"] = "123" # La clave secreta se utiliza para firmar las sesiones y garantizar la seguridad de los mensajes flash. 
app.secret_key = 'clave-secreta' # --> Ambas formás de asignación de clave son correctas
app.config['PERMANENT_SESSION_LIFETIME'] = 3600 # Manejo de expiración de la sesión. 1 hora en segundos

login_maneger = LoginManager()
login_maneger.init_app(app)
login_maneger.login_view = "loginApp.login"

@login_maneger.user_loader
def load_user(user_id):
    user_id = (str(user_id))
    user_data = db.usuarios.find_one({"_id":user_id})

    if user_data:
        user = User(user_data)
        return user
    return None


@app.route('/')
def index():
    return render_template('home.html')

app.register_blueprint(blpr)
app.register_blueprint(blpl)
app.register_blueprint(blpd)
app.register_blueprint(blpo)
app.register_blueprint(blpp)
app.register_blueprint(blpv)
app.register_blueprint(blppv)


if __name__ == "__main__":
    app.run(port=5002, debug=True)










print("Segundo commit, el Damian me sigue obligando")