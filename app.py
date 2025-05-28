from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import time
import time
import time
import time

app = Flask(__name__, static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for development, static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for development, static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for development, static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for development

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyC6a1bunkC6P8cTFYva3FIBVi-xspXhnms"
genai.configure(api_key=GEMINI_API_KEY)

# List available models to help with debugging
def list_available_models():
    try:
        models = genai.list_models()
        model_names = [model.name for model in models]
        return model_names
    except Exception as e:
        return f"Error listing models: {str(e)}"

# Initialize Gemini model - using a model from the available list
# Using gemini-1.5-flash which should have a higher quota limit
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/models')
def models():
    model_names = list_available_models()
    return jsonify({"available_models": model_names})

@app.route('/update-api-key', methods=['POST'])
def update_api_key():
    data = request.get_json()
    new_api_key = data.get('api_key', '').strip()
    
    if not new_api_key:
        return jsonify({'error': 'API key cannot be empty'}), 400
    
    try:
        # Configure with the new API key
        genai.configure(api_key=new_api_key)
        
        # Test the API key by listing models
        models = list_available_models()
        
        return jsonify({
            'success': True,
            'message': 'API key updated successfully',
            'available_models': models
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    conversation_history = data.get('history', [])
    
    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    try:
        # Create a chat session with history
        chat = model.start_chat(history=[])
        # Add conversation history to the chat
        for msg in conversation_history:
            if msg['role'] == 'user':
                chat.history.append({'role': 'user', 'parts': [msg['content']]})
            else:
                chat.history.append({'role': 'model', 'parts': [msg['content']]})
        # Add a small delay to simulate thinking (more natural conversation flow)
        time.sleep(0.5)
        # Send the user message and get response
        response = chat.send_message(user_message)
        # Format the response for better readability
        formatted_response = response.text
        return jsonify({
            'response': formatted_response
        })
    except Exception as model_error:
        error_str = str(model_error).lower()
        # Check if it's a quota error
        if "quota" in error_str or "429" in error_str:
            return jsonify({
                'error': "You've exceeded the free quota for the Gemini API. Please try again later or use a different API key.",
                'quota_exceeded': True
            }), 429
        # If there's an error with the specific model, try a fallback model
        try:
            # Try gemini-1.5-flash-latest as fallback
            fallback_model = genai.GenerativeModel("gemini-1.5-flash-latest")
            fallback_chat = fallback_model.start_chat(history=[])
            for msg in conversation_history:
                if msg['role'] == 'user':
                    fallback_chat.history.append({'role': 'user', 'parts': [msg['content']]})
                else:
                    fallback_chat.history.append({'role': 'model', 'parts': [msg['content']]})
            fallback_response = fallback_chat.send_message(user_message)
            return jsonify({
                'response': fallback_response.text,
                'note': 'Using fallback model (gemini-1.5-flash-latest)'
            })
        except Exception as fallback_error:
            try:
                # Try gemini-1.5-flash-8b as last resort
                last_resort_model = genai.GenerativeModel("gemini-1.5-flash-8b")
                last_resort_chat = last_resort_model.start_chat(history=[])
                for msg in conversation_history:
                    if msg['role'] == 'user':
                        last_resort_chat.history.append({'role': 'user', 'parts': [msg['content']]})
                    else:
                        last_resort_chat.history.append({'role': 'model', 'parts': [msg['content']]})
                last_resort_response = last_resort_chat.send_message(user_message)
                return jsonify({
                    'response': last_resort_response.text,
                    'note': 'Using basic model (gemini-1.5-flash-8b)'
                })
            except Exception as last_error:
                available_models = list_available_models()
                error_message = "Unable to use Gemini API models. This could be due to:"
                error_message += "\n1. API quota exceeded (free tier limit reached)"
                error_message += "\n2. Invalid API key"
                error_message += "\n3. Network connectivity issues"
                return jsonify({
                    'error': error_message,
                    'technical_details': f"Primary error: {str(model_error)}. Fallback error: {str(fallback_error)}. Last resort error: {str(last_error)}",
                    'available_models': available_models
                }), 500
    except Exception as e:
        return jsonify({
            'error': str(e),
            'available_models': list_available_models()
        }), 500

if __name__ == '__main__':
    app.run(debug=True)