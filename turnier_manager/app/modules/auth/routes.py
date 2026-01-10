"""
Auth Module - Routes for Admin Authentication
"""
from flask import render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import check_password_hash
from . import bp


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if session.get('is_admin'):
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        password = request.form.get('password', '')

        # Get the stored password hash from config
        stored_hash = current_app.config.get('ADMIN_PASSWORD_HASH')

        if not stored_hash:
            flash('Admin-Passwort nicht konfiguriert. Bitte ADMIN_PASSWORD_HASH setzen.', 'error')
            return render_template('pages/auth/login.html')

        # Check password against hash
        if check_password_hash(stored_hash, password):
            session['is_admin'] = True
            session.permanent = True
            flash('Erfolgreich angemeldet!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Falsches Passwort.', 'error')

    return render_template('pages/auth/login.html')


@bp.route('/logout')
def logout():
    """Logout admin"""
    session.pop('is_admin', None)
    flash('Erfolgreich abgemeldet.', 'success')
    return redirect(url_for('main.index'))


@bp.route('/generate-hash')
def generate_hash():
    """
    Helper endpoint to generate a password hash.
    Only works in debug mode for security.
    Visit /auth/generate-hash?password=your_password
    """
    if not current_app.debug:
        return 'Only available in debug mode', 403

    password = request.args.get('password')
    if not password:
        return '''
        <h1>Password Hash Generator</h1>
        <p>Add ?password=YOUR_PASSWORD to the URL to generate a hash.</p>
        <p>Then set the hash as ADMIN_PASSWORD_HASH environment variable.</p>
        ''', 200

    from werkzeug.security import generate_password_hash
    hash_value = generate_password_hash(password)

    return f'''
    <h1>Generated Hash</h1>
    <p>Password: {password}</p>
    <p>Hash:</p>
    <code style="word-break: break-all; display: block; padding: 10px; background: #f0f0f0;">
    {hash_value}
    </code>
    <p>Add this to your .env file:</p>
    <code>ADMIN_PASSWORD_HASH='{hash_value}'</code>
    ''', 200
