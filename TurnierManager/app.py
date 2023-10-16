from flask import Flask
import secrets
from routes import home, calculator, report, admin


tm = Flask(__name__, static_folder='static', template_folder='templates')
tm.secret_key = secrets.token_hex(16)


tm.register_blueprint(home.bp_home)
tm.register_blueprint(calculator.bp_calculator)
tm.register_blueprint(report.bp_report)
tm.register_blueprint(admin.bp_admin)


if __name__ == '__main__':
    tm.run(debug=True, host="0.0.0.0", port=5000)


