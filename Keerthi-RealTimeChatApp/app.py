from flask import Flask, render_template
from flask_socketio import SocketIO, send

# Create Flask app
app = Flask(__name__)

# Connect SocketIO to app
socketio = SocketIO(app)

# Homepage route
@app.route('/')
def home():
    return render_template('index.html')

# Listen for messages
@socketio.on('message')
def handle_message(data):
    print("Message received:", data)

    # Send message to all users
    send(data, broadcast=True)

# Run server
if __name__ == '__main__':
    socketio.run(app, debug=True)