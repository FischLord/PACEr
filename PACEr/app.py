from flask import Flask, render_template
import secrets
from routes import home, calculator

pacer = Flask(__name__)
pacer.secret_key = secrets.token_hex(16)


pacer.register_blueprint(home.bp_home)
pacer.register_blueprint(calculator.bp_calculator)


if __name__ == '__main__':
    pacer.run(debug=True, host="0.0.0.0", port=5000)


