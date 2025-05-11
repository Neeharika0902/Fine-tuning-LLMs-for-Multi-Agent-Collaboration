"""
Main Flask application for the Multi-Agent Chatbot system
"""
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_cors import CORS
import os
import logging
import secrets
from functools import wraps
import time

from server.multi_agent_system import setup_swarm, process_query

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generate a random secret key
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes session lifetime

# Only allow CORS for API endpoints
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize the swarm once
try:
    logger.info("Initializing global swarm...")
    global_swarm = setup_swarm()
    logger.info("Global swarm initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize global swarm: {str(e)}")
    global_swarm = None

# Store a mapping of thread_ids to their respective swarm instances
thread_swarms = {}

# In-memory user storage (replace with a database in production)
users = {
    # user: {password: password, email: user_email}
}

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:  # In production, use proper password hashing
            session['user_id'] = username
            session['login_time'] = time.time()

            # Redirect to next parameter if available
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'

    # Check if the session expired
    if request.args.get('session_expired'):
        error = 'Your session has expired. Please log in again.'

    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if username in users:
            error = 'Username already exists'
        elif password != confirm_password:
            error = 'Passwords do not match'
        else:
            # In a real app, password would be hashed
            users[username] = {
                'password': password,
                'email': email
            }
            logger.info(f"New user registered: {username}")

            # Log in the user after registration
            session['user_id'] = username
            session['login_time'] = time.time()
            return redirect(url_for('home'))

    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('login_time', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    """Serve the main application page"""
    username = session.get('user_id', 'Guest')
    user_id = session.get('user_id', 'default_user')
    return render_template('index.html', username=username, user_id=user_id)

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    try:
        data = request.json
        query = data.get('message', '')
        user_id = session.get('user_id', 'default_user')  # Use session user ID
        thread_id = data.get('thread_id', 'default_thread')

        logger.info(f"Received chat request from user {user_id}, thread {thread_id}")

        # Create a new swarm instance for each thread if it doesn't exist
        thread_key = f"{user_id}:{thread_id}"
        if thread_key not in thread_swarms:
            logger.info(f"Creating new swarm for thread {thread_key}")
            if global_swarm:
                thread_swarms[thread_key] = global_swarm
            else:
                thread_swarms[thread_key] = setup_swarm()

        # Determine agent flow based on query content
        if "python" in query.lower():
            all_trans = [
                'I need project manager agent to break down the task into 3 parts ' + query,
                'I need software engineer agent to develop the code in python with function args ' + query,
                'connect to tester to generate assert for  ' + query,
                'I need deployment engineer for documentation for  ' + query,
            ]
        elif "sql" in query.lower():
            all_trans = ['I need data engineer for '+ query]
        else:
            all_trans = []

        final_response = ''
        agent_outputs = {}
        
        if all_trans:
            # Process through all the agents in sequence
            for i in range(len(all_trans)):
                query = all_trans[i]
                response, agent_outputs = process_query(thread_swarms[thread_key], query, user_id, thread_id, agent_outputs)
                final_response += response + "\n\n"
        else:
            # Just process the single query directly
            final_response, agent_outputs = process_query(thread_swarms[thread_key], query, user_id, thread_id, {})

        return jsonify({
            'response': final_response
        })
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': str(e),
            'response': f"An error occurred while processing your request: {str(e)}"
        }), 500

@app.route('/api/reset', methods=['POST'])
@login_required
def reset_chat():
    try:
        data = request.json
        user_id = session.get('user_id', 'default_user')  # Use session user ID
        thread_id = data.get('thread_id', 'default_thread')

        # Reset the swarm for this thread
        thread_key = f"{user_id}:{thread_id}"
        if thread_key in thread_swarms:
            logger.info(f"Resetting swarm for thread {thread_key}")
            del thread_swarms[thread_key]

        return jsonify({
            'status': 'success',
            'message': 'Chat history reset'
        })
    except Exception as e:
        logger.error(f"Error in reset endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"Error resetting chat: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Backend service is running'
    })


# For running locally
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

# For WSGI
application = app
