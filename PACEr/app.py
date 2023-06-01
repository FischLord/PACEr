from flask import Flask
import secrets
from routes import home, calculator, report

pacer = Flask(__name__, static_folder='static', template_folder='templates')
pacer.secret_key = secrets.token_hex(16)


pacer.register_blueprint(home.bp_home)
pacer.register_blueprint(calculator.bp_calculator)
pacer.register_blueprint(report.bp_report)


if __name__ == '__main__':
    pacer.run(debug=True, host="0.0.0.0", port=5000)


