from flask import Flask, request, jsonify, render_template, session
import openai
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Load restaurant data
with open("restaurants.json", "r") as file:
    restaurant_data = json.load(file)

# OpenAI API key (ensure it's set in the environment)
openai.api_key = os.getenv("OPENAI_API_KEY")

class RestaurantChatbot:
    def __init__(self, data):
        self.data = data

    def get_response(self, query, price_range=None, distance=None):
        # Convert restaurant data to JSON format
        restaurants_json = json.dumps(self.data, ensure_ascii=False)

        system_message = (
            "You are a friendly restaurant recommendation chatbot. "
            "Help users find restaurants based on their preferences. "
            "Make the response engaging, start with a warm introduction, "
            "list the recommendations in a friendly way, and end by asking if they need more help."
        )

        user_message = f"I want restaurant recommendations. My preferences are:\nQuery: {query}\n"
        if price_range:
            user_message += f"Price Range: {price_range}\n"
        if distance:
            user_message += f"Distance: {distance} miles\n"

        user_message += (
            "If no restaurants match, respond with: 'Hmm, I couldn't find anything for that. "
            "Want to try something else?'"
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message + "\n\n" + restaurants_json}
                ],
                max_tokens=350,
                temperature=0.7
            )

            response_text = response["choices"][0]["message"]["content"].strip()
            return response_text if response_text else "Hmm, I couldn't find anything for that. Want to try something else?"

        except Exception as e:
            print(f"API Error: {e}")
            return "Oops! Something went wrong. Want to try again?"

# Initialize chatbot
chatbot = RestaurantChatbot(data=restaurant_data)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_conversation', methods=['GET'])
def start_conversation():
    # Start a new session for conversation flow
    session['step'] = 'food'
    return jsonify({"response": "Hi! What type of food are you craving today?"})

@app.route('/search', methods=['POST'])
def search():
    # Get user input from frontend
    user_input = request.form.get('user_input', '')
    current_step = session.get('step', 'food')

    # Start chatbot logic based on current step
    if current_step == 'food':
        session['food'] = user_input
        session['step'] = 'price_range'
        response = "Got it! What is your budget for the meal?"
    
    elif current_step == 'price_range':
        session['price_range'] = user_input
        session['step'] = 'distance'
        response = "Thanks! How far are you willing to travel? Or do you want to know restaurants open at a specific time?"
    
    elif current_step == 'distance':
        session['distance'] = user_input
        session['step'] = 'completed'
        # After collecting all info, fetch restaurant suggestions
        query = session.get('food')
        price_range = session.get('price_range')
        distance = session.get('distance')
        
        # Get recommendations from the chatbot
        response = chatbot.get_response(query, price_range, distance)
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
