from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from assistant import VoiceAssistant
import threading
import os
import time
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
# Configure for better performance
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
socketio = SocketIO(app, 
                   cors_allowed_origins="*",
                   async_mode='threading',
                   ping_timeout=60,
                   ping_interval=25,
                   max_http_buffer_size=1e8)  # 100MB max buffer size

assistant = VoiceAssistant()
assistant_running = False

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering template: {e}")
        return str(e), 500

# Add a route for static files
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@socketio.on('test_connection')
def handle_test_connection(data):
    """Test WebSocket connection"""
    print(f"Test connection received: {data}")
    emit('test_connection_response', {
        'status': 'success',
        'message': 'Connection successful',
        'server_time': datetime.datetime.now().isoformat(),
        'client_data': data
    })

@socketio.on('start_listening')
def handle_start_listening():
    global assistant_running
    if not assistant_running:
        assistant_running = True
        # Don't block the socket with speak()
        def speak_async():
            assistant.speak("I'm ready to help you. What can I do for you?")
            emit('assistant_message', {'message': "I'm ready to help you. What can I do for you?"})
        
        # Run the speak function in a separate thread
        threading.Thread(target=speak_async, daemon=True).start()

@socketio.on('user_message')
def handle_user_message(data):
    def send_response(response, error=False):
        """Helper function to send response back to client"""
        try:
            socketio.emit('assistant_message', {
                'message': response,
                'error': error
            })
            print(f"Sent response: {response[:100]}...")
            
            # Don't block on speak()
            def speak_async():
                try:
                    assistant.speak(response)
                except Exception as e:
                    print(f"Error in text-to-speech: {e}")
            
            threading.Thread(target=speak_async, daemon=True).start()
            
        except Exception as e:
            print(f"Error sending response: {e}")
            try:
                # Try one more time with a simple emit
                socketio.emit('assistant_message', {
                    'message': 'I encountered an error. Please try again.',
                    'error': True
                })
            except Exception as e2:
                print(f"Critical error sending error message: {e2}")
    
    try:
        if not data or not isinstance(data, dict):
            send_response("Invalid message format. Please try again.", error=True)
            return
            
        message = data.get('message', '').strip()
        if not message:
            send_response("I didn't receive any message. Please try again.", error=True)
            return
            
        print(f"Processing message: {message}")
        
        # Handle special commands
        message_lower = message.lower()
        if message_lower in ['exit', 'goodbye', 'bye']:
            send_response("Goodbye! Have a great day!")
            return
        
        # Process the command in a separate thread to avoid blocking
        def process_command_async():
            try:
                response = assistant.process_web_command(message)
                if not response:
                    response = "I'm not sure how to respond to that. Could you try rephrasing?"
                send_response(response)
            except Exception as e:
                error_msg = f"Error processing command: {str(e)}"
                print(error_msg)
                send_response("I'm having trouble processing your request. Please try again.", error=True)
        
        # Start the command processing in a new thread
        threading.Thread(target=process_command_async, daemon=True).start()
        
    except Exception as e:
        error_msg = f"Unexpected error in message handler: {str(e)}"
        print(error_msg)
        send_response("An unexpected error occurred. Please try again.", error=True)
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(error_msg)
        send_response("I'm sorry, something went wrong. Please try again.", error=True)

if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Check if the API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("WARNING: OPENAI_API_KEY is not set in the .env file")
    
    # Run the Flask app with optimizations
    try:
        print("Starting server...")
        print(f"Debug mode: {app.debug}")
        print(f"Templates directory: {os.path.abspath('templates')}")
        print(f"Static directory: {os.path.abspath('static')}")
        
        socketio.run(app, 
                    host='0.0.0.0',
                    port=5000,
                    debug=True,
                    use_reloader=False)  # Disable reloader for better performance
    except Exception as e:
        print(f"Failed to start server: {e}")
