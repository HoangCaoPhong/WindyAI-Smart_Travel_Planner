"""
Flask backend for session management
Runs alongside Streamlit to provide persistent sessions
"""
from flask import Flask, request, jsonify, session
from flask_session import Session
from datetime import timedelta
import secrets

app = Flask(__name__)

# Configure session
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

Session(app)

@app.route('/api/session', methods=['GET'])
def get_session():
    """Get current session data"""
    return jsonify({
        'logged_in': session.get('logged_in', False),
        'username': session.get('username', ''),
        'user_id': session.get('user_id', None)
    })

@app.route('/api/session', methods=['POST'])
def set_session():
    """Set session data"""
    data = request.json
    session['logged_in'] = data.get('logged_in', False)
    session['username'] = data.get('username', '')
    session['user_id'] = data.get('user_id', None)
    return jsonify({'success': True})

@app.route('/api/session', methods=['DELETE'])
def clear_session():
    """Clear session (logout)"""
    session.clear()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
